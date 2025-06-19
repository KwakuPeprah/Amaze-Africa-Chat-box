# chatbot.py

from fuzzywuzzy import fuzz
import string
import datetime
import json

def log_unanswered_question(question):
    """
    Logs questions that the chatbot couldn't answer to a dedicated log file.

    This helps in identifying new FAQs that might need to be added to the knowledge base.

    Args:
        question (str): The user's question that was not answered.
    """
    log_file_name = "unanswered_questions.log"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_name, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {question}\n")
    print(f"DEBUG: Logged unanswered question: '{question}' to {log_file_name}")

def log_feedback(user_question, bot_answer, feedback):
    """
    Logs user feedback (helpful/not helpful) on the bot's answers.

    This helps assess the quality of the bot's responses.

    Args:
        user_question (str): The original question asked by the user.
        bot_answer (str): The answer provided by the chatbot.
        feedback (str): The user's feedback, typically 'y' for yes or 'n' for no.
    """
    feedback_file_name = "feedback.log"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(feedback_file_name, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] Q: '{user_question}' | A: '{bot_answer}' | Helpful: {feedback}\n")
    print(f"DEBUG: Logged feedback for '{user_question}' to {feedback_file_name}")

def get_bot_response(user_question_processed, faqs):
    """
    Determines the best response for a user's question based on fuzzy matching with FAQs.

    Applies fuzzy matching to compare the user's processed question against keywords
    in the FAQ data. Handles direct matches, disambiguation for close matches,
    and returns a default 'I don't understand' message if no suitable match is found.

    Args:
        user_question_processed (str): The user's question after preprocessing (lowercase, no punctuation).
        faqs (list): A list of dictionaries, where each dictionary represents an FAQ
                      with 'keywords' and an 'answer'.

    Returns:
        str: The chatbot's response (an answer, a clarification question, or a default 'I don't understand' message).
    """
    best_match_score = 0
    potential_matches = [] 

    MATCH_THRESHOLD = 80 
    CLARIFICATION_THRESHOLD = 10 
    
    for faq_entry in faqs:
        current_faq_max_score = 0 

        for keyword in faq_entry["keywords"]:
            score = fuzz.partial_ratio(keyword, user_question_processed)

            print(f"DEBUG: Comparing keyword '{keyword}' with user input '{user_question_processed}' -> Score: {score}")
            print(f"DEBUG: Current best_match_score before potential update: {best_match_score}")

            if score > best_match_score:
                best_match_score = score

            if score > current_faq_max_score: 
                current_faq_max_score = score
        
        if current_faq_max_score >= MATCH_THRESHOLD:
            potential_matches.append({
                "faq_entry": faq_entry,
                "score": current_faq_max_score
            })

    print(f"DEBUG: Final best_match_score: {best_match_score} (Threshold: {MATCH_THRESHOLD})") 

    top_contenders = [
        match_info for match_info in potential_matches
        if match_info["score"] >= (best_match_score - CLARIFICATION_THRESHOLD)
    ]

    if len(top_contenders) == 1:
        return top_contenders[0]["faq_entry"]["answer"]
    elif len(top_contenders) > 1:
        options = [entry["faq_entry"]["keywords"][0].replace("types of ", "").title() for entry in top_contenders] 
        
        if len(options) == 2:
            clarification_question = f"It sounds like you might be asking about {options[0]} or {options[1]}? Could you please clarify?"
        else:
            clarification_question = f"It sounds like you might be asking about {', '.join(options[:-1])} or {options[-1]}? Could you please clarify?"
        return clarification_question
    else:
        log_unanswered_question(user_question_processed) 
        return "I'm sorry, I don't understand your question. Could you please rephrase or ask about common topics like hours, designs, fabric types, location, or contact?"

def run_chatbot():
    """
    Main function to run the Amaze Africa Fabrics Chatbot.

    Initializes the chatbot, loads FAQ data from 'faqs.json', and enters
    into a continuous loop to interact with the user. Handles user input
    processing, gets bot responses, and manages feedback and fallback mechanisms.
    """
    print("------------------------------------------------")
    print("Hello! Welcome to Amaze Africa Fabrics.")
    print("I can answer common questions. Type 'bye' to exit.")
    print("------------------------------------------------")

    try:
        with open('faqs.json', 'r', encoding='utf-8') as f:
            faq_data = json.load(f)
        print("DEBUG: FAQ data loaded successfully from faqs.json")
    except FileNotFoundError:
        print("ERROR: faqs.json not found! Please make sure it's in the same directory.")
        return
    except json.JSONDecodeError:
        print("ERROR: Could not decode faqs.json. Check for syntax errors in your JSON file.")
        return

    while True:
        user_input = input("You: ")

        processed_input = user_input.lower()
        processed_input = processed_input.translate(str.maketrans('', '', string.punctuation))
        processed_input = ' '.join(processed_input.split())

        print(f"DEBUG: Processed Input: '{processed_input}'")

        if processed_input == 'bye':
            print("Bot: Thank you for visiting Amaze Africa Fabrics. Goodbye!")
            break

        response = get_bot_response(processed_input, faq_data)
        print(f"Bot: {response}")

        # --- "Ask a Human" Fallback Logic ---
        if response.startswith("I'm sorry, I don't understand"):
            print("Bot: If you need further assistance, please feel free to email us at support@amasfabrics.com or call us at +233 55 123 4567 during business hours.")
        # --- END FALLBACK ---

        # --- "Was this helpful?" Feedback Prompt ---
        if not response.startswith("I'm sorry, I don't understand") and \
           not response.startswith("It sounds like you might be asking about"):
            
            feedback = input("Bot: Was this helpful? (y/n): ").strip().lower()
            if feedback in ['y', 'n']:
                log_feedback(user_input, response, feedback)
            else:
                print("Bot: Thanks for the feedback!") 
        # --- END FEEDBACK ---

if __name__ == "__main__":
    run_chatbot()