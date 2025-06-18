# chatbot.py

from fuzzywuzzy import fuzz # Importing fuzzywuzzy for fuzzy string matching
import string # Importing string for punctuation removal, which is now in use
import datetime

# --- NEW FUNCTION: Log Unanswered Questions ---
def log_unanswered_question(question):
    log_file_name = "unanswered_questions.log"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_name, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {question}\n")
    print(f"DEBUG: Logged unanswered question: '{question}' to {log_file_name}") # For immediate feedback
# -----------------------------------------------

# Make sure to import datetime at the top of your file as well!
import datetime # <-- Add this line near your other imports (fuzz, string)

def run_chatbot():
    print("------------------------------------------------")
    print("Hello! Welcome to Amaze Africa Fabrics.")
    print("I can answer common questions. Type 'bye' to exit.")
    print("------------------------------------------------")

    # New FAQ Data Structure: A list of dictionaries
    # Each dictionary contains a list of 'keywords' and the 'answer'
    faq_data = [
        {
            "keywords": ["hours", "open hours", "what time", "close"],
            "answer": "Ama's Amazing African Fabrics is open from 9 AM to 7 PM, Monday through Saturday."
        },
        {
            "keywords": ["custom designs", "design service", "unique designs"],
            "answer": "Yes, we offer custom fabric designs. Please visit our store or call us to discuss your unique needs."
        },
        {
            "keywords": ["types of fabric", "sell fabrics", "fabric types", "cloth"],
            "answer": "We specialize in authentic Kente, Ankara, and Batik fabrics."
        },
        {
            "keywords": ["location", "where are you", "address", "find you"],
            "answer": "You can find us at Osu Oxford Street, Accra, opposite the Post Office."
        },
        {
            "keywords": ["contact", "phone number", "email", "get in touch"],
            "answer": "You can call us at +233 24 123 4567 or email info@amasfabrics.com."
        },
        {
            "keywords": ["delivery", "shipping", "send"],
            "answer": "No, we do not currently offer delivery services."
        }
    ]

    # --- NEW FUNCTION FOR GETTING RESPONSE ---
    def get_bot_response(user_question_processed, faqs):

        best_match_score = 0
        best_answer = None

        MATCH_THRESHOLD = 80  # Your set threshold for fuzzy matching
        
        # Iterate through each FAQ entry in our data
        for faq_entry in faqs:

            # Check each keyword associated with the current FAQ entry
            for keyword in faq_entry["keywords"]:
                score = fuzz.partial_ratio(keyword, user_question_processed)

                # --- DEBUG PRINTS: CORRECTLY PLACED INSIDE THE INNER LOOP ---
                print(f"DEBUG: Comparing keyword '{keyword}' with user input '{user_question_processed}' -> Score: {score}")
                print(f"DEBUG: Current best_match_score before potential update: {best_match_score}")
                # -----------------------------------------------------------

                if score > best_match_score:
                    best_match_score = score
                    best_answer = faq_entry["answer"]
        
        # --- DEBUG PRINT: After all loops have completed ---
        print(f"DEBUG: Final best_match_score: {best_match_score} (Threshold: {MATCH_THRESHOLD})") 
        # --------------------------------------------------

        if best_match_score >= MATCH_THRESHOLD:
            return best_answer
        else:
            # If no keyword matched well enough, return a default response
            log_unanswered_question(user_question_processed)  # Log the unanswered question
            return "I'm sorry, I don't understand your question. Could you please rephrase or ask about common topics like hours, designs, fabric types, location, or contact?"


    while True:
        user_input = input("You: ")

        # Process the input to lower case
        processed_input = user_input.lower()

        # Remove punctuation
        processed_input = processed_input.translate(str.maketrans('', '', string.punctuation))

        # Normalize whitespace
        processed_input = ' '.join(processed_input.split())

        # --- DEBUG PRINT: To see the cleaned input ---
        print(f"DEBUG: Processed Input: '{processed_input}'")
        # ---------------------------------------------

        if processed_input == 'bye':
            print("Bot: Thank you for visiting Amaze Africa Fabrics. Goodbye!")
            break

        # Call our new function to get the bot's response
        response = get_bot_response(processed_input, faq_data)
        print(f"Bot: {response}")

if __name__ == "__main__":
    run_chatbot()