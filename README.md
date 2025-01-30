# 🤖 SILLY.py - Simple Chatbot for Customer Support (Proof of Concept)

SILLY (**Straightforward Interactive Language Yapper**) is a proof-of-concept chatbot designed to assist customers with common support inquiries. Using Natural Language Processing (NLP) techniques, it recognizes keywords, matches predefined responses, and generates support tickets. SILLY can handle issues like updates, returns, and agent escalation requests. Although it’s a basic implementation, it provides a functional customer support experience with logs for record-keeping.

This project demonstrates basic chatbot functionality, focusing on keyword matching and automated responses.

---

## ✨ Features
- **Keyword Matching**: Scans user input to identify intent based on predefined support topics.
- **NLP-enhanced**: Uses the NLTK library to recognize synonyms for better intent matching.
- **Conversation Logging**: Records interactions for future analysis and review.
- **Ticket Generation**: Automatically creates a basic text-based support ticket.
- **Escalation to Agent**: Allows complex issues to be escalated to a human support agent.
- **Caching**: Stores dictionary of topics for faster future interactions.

## 🔧 Prerequisites
- **Python 3.x**: Ensure Python 3.x is installed on your system.
- **Install Dependencies**: Run the following command to install the necessary Python libraries:
  ```sh
  pip install nltk
  ```

## 🚀 Setup and Usage

1. **Clone the repository**:
   ```sh
   git clone https://github.com/urban05/SILLY-proof-of-concept-chatbot/
   cd SILLY-proof-of-concept-chatbot
   ```

2. **Run the chatbot**:
   ```sh
   python SILLY.py
   ```

3. The chatbot will initialize and begin interacting with users.

## 🛠️ Functionality
- **Keyword Matching**: SILLY processes user input to match predefined topics and responds with relevant information.
- **Predefined Scripts**: Handles common support inquiries such as software updates and product returns.
- **Conversation Logging**: Logs all interactions in text files for future analysis.
- **Ticket Generation**: Generates a simple support ticket with customer details, facilitating issue tracking.

## 📂 File Structure
```
SILLY-proof-of-concept-chatbot/
│── SILLY.py                  # Main chatbot script
│── silly_topics_cache.txt    # Cached topics for faster processing
│── [...]_SILLYlog.txt        # Conversation logs
│── [...]_ticket.txt          # Generated tickets
│── testSILLY.py              # Unit testing script (Proof of Concept)
```

## 📚 Example Interaction
```
---------- SILLY CONNECTED ----------
SILLY: Welcome to Customer Support! I am SILLY (Straightforward Interactive Language Yapper). How can I help you today?
You: I can't update my product.
SILLY: It seems like you have trouble updating your product. Is that right? (yes/no)
You: Yup
SILLY: If you're experiencing issues updating your product, please follow these steps...
```

## 🔮 Future Enhancements
- **Email Integration**: Integration with an e-mail server, to send out e-mails.
- **Ticketing System Integration**: Integrate with a ticket management system.
- **Web Interface**: Implement a user-friendly web interface for smoother interactions.
- **More Support Cases**: Implement more cases for common issues. Differentiate based on the product the customer is inquiring about.

## 📄 License
This project is licensed under the MIT License. See the `LICENSE` file for more information.
