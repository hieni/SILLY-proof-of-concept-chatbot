#SILLY.py - a simple chatbot for cutomer support - Proof of Concept
### Setup ###
print("\n\n----------\nSILLY 1.0\nChecking dependencies")
try:
    import nltk
except: 
    print("\n\nModuleNotFoundError: No module named 'nltk'\nInstall it using:\n\n    py -m pip install nltk\n\n")

import os
import re
import random
import string
import json
from datetime import datetime
from nltk.corpus import wordnet as wn

nltk.download('wordnet')

TOPICS_CACHE_FILE = "silly_topics_cache.txt" # point to cache file

logs = []           # create empty log
topics = {}         # create empty list of topics
ticket_id = None    # create empty ticket_id


print("Done!\n----------\n\n")

# add log entry
def add_log(message, logs=logs):                # ask for which log to write to and which message
    logs.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

debug = True
if debug: 
    print("\nSYSTEM: SILLY STARTED IN DEBUG MODE\n")
    add_log(f"SYSTEM: SILLY STARTED IN DEBUG MODE")

### Exception to EXIT chatbot
class ExitChatbotException(Exception):
    pass

### Define Functions ###
# Dump topics to cache
def save_topics(topics):
    with open(TOPICS_CACHE_FILE, "w") as f:
        json.dump(topics, f)

# Load topics from cache
def load_topics():
    if os.path.exists(TOPICS_CACHE_FILE):
        with open(TOPICS_CACHE_FILE, "r") as f:
            return json.load(f)
    return None

#initialize bot
def init_bot(silent=None):
    if silent is None: 
        print("\n\n----------\nInitializing SILLY, please wait...")
    global topics

    # Check if topics cache exists
    cached_topics = load_topics()
    if cached_topics:
        topics = {k: set(v) for k, v in cached_topics.items()}  # Convert lists back to sets
        add_log(f"SYSTEM: LOADED TOPIC FROM CACHE.")
        if debug:
            print(f"\nDEBUG:\nDictionary contains:\n{topics}\n")
        if silent is None: 
            print("Done!\n----------\n\n")
        return
    
    add_log(f"SYSTEM: BUILDING TOPIC LIST")    
    
    # manually broaden meaning of synonym for certain words 
    synonyms_agent = find_synonyms("human") | find_synonyms("agent") | find_synonyms("manager") | find_synonyms("employee")
    synonyms_email = find_synonyms("email") | find_synonyms("mail")
    synonyms_phone = find_synonyms("telephone") | find_synonyms("phone")
    
    # build dictionary containing sets of topics that the bot can help with
    topics = {
        "agent": synonyms_agent,
        "update": find_synonyms("update"),
        "return": find_synonyms("return"),
        "yes": find_synonyms("yes") | {"y", "yeah", "yup", "sure"},
        "email": synonyms_email,
        "phone": synonyms_phone
    }
    
    # Save topics to cache file
    save_topics({k: list(v) for k, v in topics.items()})
    add_log(f"SYSTEM: SAVED TOPICS TO CACHE.")
    
    if debug:
        print(f"\nDEBUG:\nDictionary contains:\n{topics}\n")

    if silent is None: 
        print("Done!\n----------\n\n")


# Find Synonym for entered word
def find_synonyms(word):                            # takes a single word
    synonyms = set()                                # list synonyms in a set, to avoid duplicates
    for syn in wn.synsets(word):                    # for every synonym (broad meaning of a word)
        for lemma in syn.lemmas():                  # add each lemma (specific synonym) to set
            lemma_name = lemma.name().lower()
            if "_" in lemma_name:                   # check if the synonym contains an underscore
                synonyms.update(lemma_name.split('_'))  # split by underscore and add both parts
            else:
                synonyms.add(lemma_name)            # add the synonym as is
    return synonyms

# save log to file
def save_log(logs, filename):
    with open(filename, 'w') as f:
        f.write("\n".join(logs))

# get a "unique" ticket ID
def generate_ticket_id():
    #based on the current date, hour and 4 random letters
    current_time = datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")  
    hour_str = current_time.strftime("%H")
    random_letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    
    # Combine data to final ID
    ticket_id = f"{date_str}-{hour_str}{random_letters}"
    return ticket_id

# hand in a ticket to a support agent
# TODO: Integrate actual sending of email, if this wasn't out of scope for this assignment
def create_ticket(ticket_id, issue, email, telephone, preference):
    # save it as a text file as a proof of concept
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
    
    # Write the content to a text file
    with open(ticket_filename, 'w') as f:
        f.write(ticket_content)
    add_log(f"INFO: SILLY created ticked {ticket_id}")

# conversation shortcuts
def bot_print(bot_sentence):
    print (f"SILLY: {bot_sentence}")
    add_log (f"SILLY: {bot_sentence}")
def customer_input():
    c_input = input("You: ")
    add_log (f"Customer: {c_input}")
    if c_input == "EXIT":
        raise ExitChatbotException
    return c_input

# keyword search
def keyword_search(searchterm):
    keywords = searchterm.lower().split()               # generate list of words entered by customer
    matched_topic = None
    for topic, synonyms in topics.items():              # iterate over topic dictionary
        if any(word in synonyms for word in keywords):  # iterate over keywords and look for first match in dictionary
            matched_topic = topic                       # match topic, if any
            return matched_topic


# validate input
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'                   # regular expression for mail format (something@something.something)
    return bool(re.match(pattern, email))

def validate_phone(phone):
    return bool(re.match(r'^[\d\s\-\+\(\)]+$', phone)) and any(char.isdigit() for char in phone)  # Allow only digits, plusses, minusses, brackets, dashes or spaces an ensure at least one digit

# pre-define scripts
def case_update():
    bot_print("If you're experiencing issues updating your product, please follow these steps:\n1. Ensure you have an active internet connection.\n2. Restart the application and try updating again.\n3. Check for any error messages.\n4. Visit our support page for detailed troubleshooting steps.\n\nHave you resolved the issue? (yes/no)")
    if keyword_search(customer_input()) != "yes":
        bot_print("Alright, I will create a ticket with our support.")
        case_agent("update")
    else:
        bot_print("Alright, thank you for contacting BUGLAND")
        add_log(f"INFO: Issue resolved. No Ticket will be submitted, but log will be kept for analytics purpose")

def case_return():
    bot_print("If you'd like to return your product straight away, please ensure:\n1. You have the serial number.\n2. The product was purchased within the last 14 days.\n\nDo you have your serial number and purchased the product in the last 14 days? (yes/no)")
    if keyword_search(customer_input()) != "yes":           # Transfer customer to support agent, if they have troubles locating serial number or are not certainly under return policy
        bot_print("Alright, I will transfer you to our support.")
        case_agent("Return")
    else:                                                   # Send email to customer for return shipping and open ticket at BUGLAND
        bot_print("Okay, please enter your serial number")
        serial_number = customer_input().upper()   #TODO: check if serialnumber actually exists in asset management system, if this wasn't out of scope of this assignment
        bot_print("I am quickly checking, if your product was pruchased within the last 14 days. Please wait...")
        add_log(f"INFO: Serialnumber is {serial_number}")
        add_log(f"SYSTEM: CHECKING DATE OF PURCASE OF PRODUCT {serial_number}")
        add_log(f"DEBUG: Would hand off serial number to asset management system and check, if date of purchase is no more than 14 days away")
        #TODO: Integration with asset management system, if this wasn't out of scope of this assignment
        under_warranty = True
        if under_warranty:
            bot_print("Your product can be returned right away. You will recieve your refund, once it has arrived back at BUGLAND and we've checked, that it wasn't intentionally or negligently damaged. I will send you the return shipping lable. \nPlease enter you e-mail address:")
            email = ""
            while True:
                email = customer_input().strip()
                if validate_email(email):
                    break
                else:
                    bot_print("Invalid email format. Please enter a valid email.")
            create_ticket(ticket_id,"APPROVED RETURN",email,"","")
            add_log(f"INFO: SILLY automatically approved return for {serial_number}")
            #TODO: Integration with logistics system, to actually send out a return lable, if this wasn't out of scope of this assignment
            bot_print("Thank you! The return shipping lable should arrive shortly.")
        else:   # Transfer to support agent, if not under return policy
            bot_print("It seems, like that your product is not covered under our return policy anymore. I will transfer you to one of our support agents for further assistance.")
            case_agent("return outside policy")

def case_agent(topic=None):
    if topic is None:
        topic = "misc"
    # Get valid email or allow the user to skip
    email = ""
    while True:
            bot_print("Enter your email address (or leave blank to skip):")
            email = customer_input().strip()
            if email == "" or validate_email(email):
                break
            else:
                bot_print("Invalid email format. Please enter a valid email.")

    # Get a valid telephone number or allow the user to skip
    telephone = ""
    while True:
        bot_print("Enter your telephonenumber (or leave blank to skip)")
        telephone = customer_input().strip()
        if telephone == "" or validate_phone(telephone):
            break
        else:
            bot_print("Invalid phone number format. Please enter a valid phone number.")

    # Ensure at least one contact method is provided
    if not email and not telephone:
        bot_print("You must provide at least one way to contact you. Please enter either an email or a phone number.")
        return case_agent()  # Restart the function

    # If both methods were entered, ask for preferred method of contact
    preference = ""
    if email and telephone:
        while True:
            bot_print("Which is your preferred method of contact? (email/phone)")
            preference_input = customer_input().strip().lower()
            matched_preference = keyword_search(preference_input)  # Use keyword matching

            if matched_preference in ["email", "phone"]:
                preference = matched_preference
                break
            else:
                bot_print("Please enter 'email' or 'phone'.")

    # Create ticket with entered informations
    create_ticket(ticket_id, topic, email, telephone, preference)
    bot_print("I have created a ticket with our support agent, they will be in touch shortly.")

# Check back, if the bot understood the customer, if it did return true
def clarification(keywords,topic):
    if keyword_search(customer_input()) != "yes":
        # remove topic, if user says no
        del topics[topic]
        bot_print("Thank you for the clarification! Let me try re-processing your Input, please wait...")
        issue_match(keywords)
    else: 
        return True

# match issue with pre-defined scripts
def issue_match(keywords=None):
    if keywords is None:
        keywords = customer_input()                 # Get initial input if not provided
    issue = keyword_search(keywords)

    match issue:
        case "update":
            bot_print("It seems like you have troubles updating your product.\nIs that right? (yes/no)")
            if clarification(keywords,"update") == True:
                case_update()
            
        case "return":
            bot_print("It seems like you want to return your product. \nIs that right? (yes/no)")
            if clarification(keywords,"return") == True:
                case_return()

        case "agent":
            bot_print("It seems like you want to talk to a live agent. \nIs that right? (yes/no)")
            if clarification(keywords,"agent") == True:
                bot_print("Alright, I will create a Ticket.")
                case_agent()            

        case _:
            init_bot("silent")
            bot_print("I am sorry, I did not understand that. Please try explaining your problem again. Type 'EXIT' to exit")
            issue_match()



### chatbot function ###
def chatbot():
    try:
        init_bot()

        print("---------- SILLY CONNECTED ----------")
        # give conversation a Ticket ID
        global ticket_id 
        ticket_id = generate_ticket_id()
        add_log(f"INFO: Ticket-ID is {ticket_id}")

        # initial exchange
        bot_print("Welcome to Customer Support! I am SILLY (Straightforward Interactive Language Yapper) How can I help you today?")
    
        # Let the costumer input their issue and try to match it to the dictionary and pre-defined scripts
        issue_match()
    
    except ExitChatbotException:
        bot_print("I am deeply sorry I couldn't help.")
        add_log(f"SYSTEM: CONVERSATION EXITED, DISCARDING TICKET. KEEPING LOG FOR ANALYTICS")
    
    finally:
        # save log to file
        add_log(f"SYSTEM: END OF CONVERSATION, SAVING LOG")
        log_file = f"{ticket_id}_SILLYlog.txt"
        save_log(logs, log_file)
        if debug: print(f"\n\nConversation log saved to {log_file}.\n\n")
        print("---------- SILLY DISCONNECTED ----------")

    




### start chatbot ###
chatbot()
