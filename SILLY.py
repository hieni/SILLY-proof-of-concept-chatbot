#SILLY.py - a simple chatbot for customer support - Proof of Concept

### Setup ###
print("\n\n----------\nSILLY 1.0\nChecking dependencies")

# Try to import necessary NLTK module, handle errors if the module is missing
try:
    import nltk
except: 
    print("\n\nModuleNotFoundError: No module named 'nltk'\nInstall it using:\n\n    py -m pip install nltk\n\n")

# Import other required modules for system operations, regex, random generation, JSON handling, datetime, and NLTK WordNet
import os
import re
import random
import string
import json
from datetime import datetime
from nltk.corpus import wordnet as wn

# Ensure WordNet data is downloaded
nltk.download('wordnet')

# Path for storing cached topics data
TOPICS_CACHE_FILE = "silly_topics_cache.txt"

# Initialize logs and topics as empty structures, also create an empty ticket ID
logs = []           # List to store log messages
topics = {}         # Dictionary to hold topics the bot can discuss
ticket_id = None    # Placeholder for customer ticket ID

print("Done!\n----------\n\n")

# Function to log messages to the logs list with a timestamp
def add_log(message, logs=logs):
    logs.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# Debug mode flag to show additional internal messages for development purposes
debug = True
if debug: 
    print("\nSYSTEM: SILLY STARTED IN DEBUG MODE\n")
    add_log(f"SYSTEM: SILLY STARTED IN DEBUG MODE")

### Custom exception class to exit chatbot
class ExitChatbotException(Exception):
    pass

### Define Functions ###

# Function to save the current topics dictionary to a file (cache)
def save_topics(topics):
    with open(TOPICS_CACHE_FILE, "w") as f:
        json.dump(topics, f)

# Function to load the cached topics from file, if it exists
def load_topics():
    if os.path.exists(TOPICS_CACHE_FILE):
        with open(TOPICS_CACHE_FILE, "r") as f:
            return json.load(f)
    return None

# Function to initialize the chatbot
def init_bot(silent=None):
    # Print initializing message if silent flag is not set
    if silent is None: 
        print("\n\n----------\nInitializing SILLY, please wait...")
    
    global topics  # Access global topics variable to store the list of topics

    # Try to load previously saved topics from cache if available
    cached_topics = load_topics()
    if cached_topics:
        # If cache exists, convert cached lists back to sets for easier manipulation
        topics = {k: set(v) for k, v in cached_topics.items()}  
        add_log(f"SYSTEM: LOADED TOPIC FROM CACHE.")
        
        # In debug mode, print detailed information about the loaded topics
        if debug:
            debug_message = f"DEBUG:\nDictionary contains:\n{topics}\n"
            print(debug_message)  # Print debug message
            add_log(debug_message)  # Log debug message
        
        if silent is None: 
            print("Done!\n----------\n\n")
        return
    
    # If no cached topics, build a fresh list of topics for the bot
    add_log(f"SYSTEM: BUILDING TOPIC LIST")    
    
    # Manually define and expand synonyms for certain words to ensure better understanding
    synonyms_agent = find_synonyms("human") | find_synonyms("agent") | find_synonyms("manager") | find_synonyms("employee")
    synonyms_email = find_synonyms("email") | find_synonyms("mail")
    synonyms_phone = find_synonyms("telephone") | find_synonyms("phone")
    
    # Build a dictionary that maps topics to sets of synonyms, making it easier to match user input
    topics = {
        "agent": synonyms_agent,
        "update": find_synonyms("update"),
        "return": find_synonyms("return"),
        "yes": find_synonyms("yes") | {"y", "yeah", "yup", "sure"},  # Synonyms for affirmation
        "email": synonyms_email,
        "phone": synonyms_phone
    }
    
    # Save the built topics list to the cache file for future use
    save_topics({k: list(v) for k, v in topics.items()})
    add_log(f"SYSTEM: SAVED TOPICS TO CACHE.")
    
    # In debug mode, print detailed information about the topics dictionary
    if debug:
        debug_message = f"DEBUG:\nDictionary contains:\n{topics}\n"
        print(debug_message)  # Print debug message
        add_log(debug_message)  # Log debug message 

    # Print final initialization message
    if silent is None: 
        print("Done!\n----------\n\n")

# Find Synonym for entered word
def find_synonyms(word):                            # Function takes a single word as input
    synonyms = set()                                # Initialize an empty set to store synonyms (sets avoid duplicates)
    for syn in wn.synsets(word):                    # Iterate through each WordNet synset (broad meaning of the word)
        for lemma in syn.lemmas():                  # For each lemma (specific synonym) in the synset
            lemma_name = lemma.name().lower()       # Get the lemma's name and convert it to lowercase
            if "_" in lemma_name:                   # If the synonym contains an underscore (e.g., "data_processing")
                synonyms.update(lemma_name.split('_'))  # Split by underscore and add both parts as individual words
            else:
                synonyms.add(lemma_name)            # Otherwise, add the synonym as is
    return synonyms                                 # Return the set of synonyms

# Save log to file
def save_log(logs, filename):
    with open(filename, 'w') as f:
        f.write("\n".join(logs))                      # Write the log entries to a file, joining them with newlines

# Generate a "unique" ticket ID
def generate_ticket_id():
    # Based on the current date, hour, and 4 random letters
    current_time = datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")  # Format the current date
    hour_str = current_time.strftime("%H")         # Format the current hour
    random_letters = ''.join(random.choices(string.ascii_uppercase, k=4))  # Generate 4 random uppercase letters
    
    # Combine the date, hour, and random letters into the final ticket ID
    ticket_id = f"{date_str}-{hour_str}{random_letters}"
    return ticket_id                             # Return the generated ticket ID

# Create a support ticket (for proof of concept, saves as a text file)
# TODO: Integrate actual sending of email
def create_ticket(ticket_id, issue, email, telephone, preference):
    # Create the ticket content to be saved in a text file
    ticket_filename = f"{ticket_id}_ticket.txt"
    ticket_content = f"""
From: silly@bugland.com
To: level1@bugland.com
Subject: {ticket_id}

Message:
    Ticket ID: {ticket_id}
    Issue: {issue}
    Customer Email: {email}
    Customer Telephone: {telephone}
    Preferred Contact: {preference}
    """
    
    # Write the ticket content to a text file
    with open(ticket_filename, 'w') as f:
        f.write(ticket_content)
    add_log(f"INFO: SILLY created ticket {ticket_id}")  # Log that the ticket was created

# Print bot's message and log it
def bot_print(bot_sentence):
    print(f"SILLY: {bot_sentence}")   # Print the bot's message
    add_log(f"SILLY: {bot_sentence}")  # Log the bot's message

# Get customer input, log it, and handle exit
def customer_input():
    c_input = input("You: ")             # Get the customer's input
    add_log(f"Customer: {c_input}")      # Log the customer's input
    if c_input == "EXIT":                # If the input is "EXIT", raise an exception to exit the chatbot
        raise ExitChatbotException
    return c_input                        # Return the customer's input

# Keyword search to match customer query with bot's topics
def keyword_search(searchterm):
    keywords = searchterm.lower().split()           # Split the entered search term into lowercase keywords
    matched_topic = None
    for topic, synonyms in topics.items():          # Iterate over the bot's topics and their synonyms
        if any(word in synonyms for word in keywords):  # Check if any of the entered keywords match the synonyms for a topic
            matched_topic = topic                    # If a match is found, set the matched topic
            return matched_topic                     # Return the matched topic

# Validate email format using regular expression
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Regular expression pattern for a valid email address
    return bool(re.match(pattern, email))  # Return True if the email matches the pattern, otherwise False

# Validate phone number format (allows digits, spaces, hyphens, parentheses, and plusses)
def validate_phone(phone):
    # Regular expression for validating phone number
    return bool(re.match(r'^[\d\s\-\+\(\)]+$', phone)) and any(char.isdigit() for char in phone)  # Ensure at least one digit is present

# Pre-defined scripts for handling various customer issues

def case_update():
    # Steps for assisting with product update issues
    bot_print("If you're experiencing issues updating your product, please follow these steps:\n1. Ensure you have an active internet connection.\n2. Restart the application and try updating again.\n3. Check for any error messages.\n4. Visit our support page for detailed troubleshooting steps.\n\nHave you resolved the issue? (yes/no)")
    if keyword_search(customer_input()) != "yes":  # If the customer hasn't resolved the issue
        bot_print("Alright, I will create a ticket with our support.")
        case_agent("update")  # Transfer to agent for assistance
    else:
        bot_print("Alright, thank you for contacting BUGLAND")
        add_log(f"INFO: Issue resolved. No Ticket will be submitted, but log will be kept for analytics purpose")

def case_return():
    # Handle product return inquiries
    bot_print("If you'd like to return your product straight away, please ensure:\n1. You have the serial number.\n2. The product was purchased within the last 14 days.\n\nDo you have your serial number and purchased the product in the last 14 days? (yes/no)")
    if keyword_search(customer_input()) != "yes":  # If there are issues with serial number or return eligibility
        bot_print("Alright, I will transfer you to our support.")
        case_agent("Return")  # Transfer to agent for further assistance
    else:
        bot_print("Okay, please enter your serial number")
        serial_number = customer_input().upper()  # Get serial number from customer
        bot_print("I am quickly checking, if your product was purchased within the last 14 days. Please wait...")
        add_log(f"INFO: Serialnumber is {serial_number}")
        add_log(f"SYSTEM: CHECKING DATE OF PURCHASE OF PRODUCT {serial_number}")
        add_log(f"DEBUG: Would hand off serial number to asset management system and check, if date of purchase is no more than 14 days away")
        
        # TODO: Integrate with asset management system to check purchase date
        under_warranty = True  # Simulated result of purchase check

        if under_warranty:
            bot_print("Your product can be returned right away. You will receive your refund, once it has arrived back at BUGLAND and we've checked, that it wasn't intentionally or negligently damaged. I will send you the return shipping label. \nPlease enter your e-mail address:")
            email = ""
            while True:
                email = customer_input().strip()
                if validate_email(email):  # Validate the email entered by the customer
                    break
                else:
                    bot_print("Invalid email format. Please enter a valid email.")
            create_ticket(ticket_id, "APPROVED RETURN", email, "", "")  # Create a ticket for the return
            add_log(f"INFO: SILLY automatically approved return for {serial_number}")
            # TODO: Integration with logistics system to send return label
            bot_print("Thank you! The return shipping label should arrive shortly.")
        else:
            # If not under warranty, transfer to agent for further assistance
            bot_print("It seems your product is not covered under our return policy anymore. I will transfer you to one of our support agents for further assistance.")
            case_agent("return outside policy")

def case_agent(topic=None):
    # Handle customer cases that require agent involvement
    if topic is None:
        topic = "misc"
    
    # Get valid email address or allow user to skip
    email = ""
    while True:
        bot_print("Enter your email address (or leave blank to skip):")
        email = customer_input().strip()
        if email == "" or validate_email(email):  # Validate email format
            break
        else:
            bot_print("Invalid email format. Please enter a valid email.")
    
    # Get valid phone number or allow user to skip
    telephone = ""
    while True:
        bot_print("Enter your telephone number (or leave blank to skip)")
        telephone = customer_input().strip()
        if telephone == "" or validate_phone(telephone):  # Validate phone number format
            break
        else:
            bot_print("Invalid phone number format. Please enter a valid phone number.")
    
    # Ensure at least one contact method is provided
    if not email and not telephone:
        bot_print("You must provide at least one way to contact you. Please enter either an email or a phone number.")
        return case_agent()  # Restart if no contact details provided
    
    # Ask for preferred method of contact if both email and phone are provided
    preference = ""
    if email and telephone:
        while True:
            bot_print("Which is your preferred method of contact? (email/phone)")
            preference_input = customer_input().strip().lower()
            matched_preference = keyword_search(preference_input)  # Match preference with keywords
            if matched_preference in ["email", "phone"]:
                preference = matched_preference
                break
            else:
                bot_print("Please enter 'email' or 'phone'.")
    
    # Create a support ticket with the provided information
    create_ticket(ticket_id, topic, email, telephone, preference)
    bot_print("I have created a ticket with our support agent, they will be in touch shortly.")

# Function to clarify customer input if necessary
def clarification(keywords, topic):
    if keyword_search(customer_input()) != "yes":
        # Remove topic from the dictionary if customer says no
        del topics[topic]
        bot_print("Thank you for the clarification! Let me try re-processing your input, please wait...")
        issue_match(keywords)  # Reattempt to match the issue
    else:
        return True

# Function to match issues to predefined scripts
def issue_match(keywords=None):
    if keywords is None:
        keywords = customer_input()  # Get initial input if not provided
    issue = keyword_search(keywords)

    match issue:
        case "update":
            bot_print("It seems like you have troubles updating your product.\nIs that right? (yes/no)")
            if clarification(keywords, "update") == True:
                case_update()
            
        case "return":
            bot_print("It seems like you want to return your product. \nIs that right? (yes/no)")
            if clarification(keywords, "return") == True:
                case_return()

        case "agent":
            bot_print("It seems like you want to talk to a live agent. \nIs that right? (yes/no)")
            if clarification(keywords, "agent") == True:
                bot_print("Alright, I will create a Ticket.")
                case_agent()
            
        case _:
            init_bot("silent")
            bot_print("I am sorry, I did not understand that. Please try explaining your problem again. Type 'EXIT' to exit")
            issue_match()  # Retry if no match found

### Chatbot function ###
def chatbot():
    try:
        init_bot()  # Initialize the bot

        print("---------- SILLY CONNECTED ----------")
        # Assign a Ticket ID for the conversation
        global ticket_id
        ticket_id = generate_ticket_id()
        add_log(f"INFO: Ticket-ID is {ticket_id}")

        # Initial exchange with the customer
        bot_print("Welcome to Customer Support! I am SILLY (Straightforward Interactive Language Yapper). How can I help you today?")
    
        # Let the customer input their issue and try to match it to predefined scripts
        issue_match()
    
    except ExitChatbotException:
        bot_print("I am deeply sorry I couldn't help.")
        add_log(f"SYSTEM: CONVERSATION EXITED, DISCARDING TICKET. KEEPING LOG FOR ANALYTICS")
    
    finally:
        # Save the conversation log to a file
        add_log(f"SYSTEM: END OF CONVERSATION, SAVING LOG")
        log_file = f"{ticket_id}_SILLYlog.txt"
        save_log(logs, log_file)
        if debug:
            print(f"\n\nConversation log saved to {log_file}.\n\n")
        print("---------- SILLY DISCONNECTED ----------")

# Start the chatbot
chatbot()
