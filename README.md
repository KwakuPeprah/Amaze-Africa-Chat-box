# Amaze Africa Fabrics Chatbot

## Project Overview

This project is a basic yet robust chatbot designed to answer frequently asked questions (FAQs) for "Amaze Africa Fabrics." The bot leverages fuzzy string matching to understand user queries, provides disambiguation when questions are ambiguous, and offers a helpful fallback for unanswerable questions. Its knowledge base is externalized in a JSON file for easy management and updates.

## Features

* **Intelligent Matching:** Uses `fuzzywuzzy` to perform fuzzy string matching, allowing the bot to understand user questions even with slight variations, typos, or incomplete phrases.
* **Contextual Disambiguation:** When a user's question closely matches multiple FAQs, the bot intelligently asks for clarification to provide the most accurate answer.
* **Externalized Knowledge Base:** All FAQs are stored in a separate `faqs.json` file, making the chatbot's knowledge base easy to update and expand without modifying the core Python code.
* **Unanswered Question Logging:** Automatically logs questions the bot couldn't answer to `unanswered_questions.log`, helping identify gaps in the FAQ data for continuous improvement.
* **User Feedback Mechanism:** After providing an answer, the bot asks the user if the response was helpful, logging feedback to `feedback.log` for quality assessment.
* **"Ask a Human" Fallback:** If the bot cannot answer a question, it provides contact information (email and phone) for users to reach out to human support.
* **Clean & Modular Code:** The project is structured with clear functions, enhancing readability and maintainability.

## Setup

To run this chatbot, you'll need Python installed on your system.

1.  **Clone or Download the Project:**
    (If you have a Git repository, `git clone <repository-url>`. Otherwise, download the project files.)

2.  **Navigate to the Project Directory:**
    Open your terminal or command prompt and change to the directory where you saved `chatbot.py`, `faqs.json`, and `README.md`.

    ```bash
    cd path/to/your/chatbot-project
    ```

3.  **Install Dependencies:**
    This project uses the `fuzzywuzzy` library. You can install it using pip:

    ```bash
    pip install fuzzywuzzy[speedup]
    ```
    *Note: `[speedup]` includes `python-Levenshtein` for faster processing, which is recommended but optional.*

4.  **Ensure `faqs.json` exists:**
    Make sure the `faqs.json` file is in the same directory as `chatbot.py`. This file contains all your chatbot's knowledge.

## Usage

To start the chatbot, simply run the `chatbot.py` script from your terminal:

```bash
python chatbot.py