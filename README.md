# SILLY.py - Simple Chatbot for Customer Support (Proof of Concept)

## Overview
SILLY (**Straightforward Interactive Language Yapper**) is a proof-of-concept chatbot designed to assist customers with common support inquiries. It uses NLP techniques to recognize keywords, match predefined responses, and create support tickets. The bot can handle update issues, returns, and agent escalation requests while logging conversations for record-keeping.

## Features
- Recognizes user queries and maps them to predefined support topics.
- Uses the NLTK library to find synonyms for improved keyword matching.
- Generates and stores conversation logs for analysis.
- Provides a basic proof-of-concept ticketing system.
- Can escalate complex issues to a human agent.
- Simple caching system for topic recognition.

## Requirements
- Python 3.x
- Required dependencies:
  ```sh
  pip install nltk
  ```

## Setup & Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/SILLY.git
   cd SILLY
   ```
2. Run the chatbot:
   ```sh
   python SILLY.py
   ```
3. The chatbot initializes, loads cached topics (if available), and interacts with users.

## Functionality
- **Keyword Matching:** SILLY scans user input and determines the intent based on predefined topics.
- **Predefined Scripts:** Covers support cases such as software updates and returns.
- **Conversation Logging:** Logs interactions in text files for later review.
- **Ticket Generation:** Creates a simple text-based support ticket with customer details.

## File Structure
```
SILLY/
│── SILLY.py                  # Main chatbot script
│── silly_topics_cache.txt    # Cached topics for faster processing
│── [...]SILLYlog.txt         # Conversation logs
│── [...]Ticket.txt           # Generated tickets
```

## Example Interaction
```
---------- SILLY CONNECTED ----------
SILLY: Welcome to Customer Support! How can I help you today?
You: I can't update my product.
SILLY: It seems like you have trouble updating your product. Is that right? (yes/no)
You: Yes
SILLY: Please follow these steps...
```

## Future Enhancements
- Implementing an email-sending feature for support tickets.
- Connecting to an actual ticketing system (e.g., Zendesk, Jira).
- GUI or web-based interface for easier use.

## License
This project is released under the MIT License.
