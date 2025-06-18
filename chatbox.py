# chatbot.py

from fuzzywuzzy import fuzz # Importing fuzzywuzzy for fuzzy string matching
import string # Importing string for punctuation removal, which is now in use
import datetime # Importing datetime for logging timestamps

# --- NEW FUNCTION: Log Unanswered Questions ---
def log_unanswered_question(question):
    log_file_name = "unanswered_questions.log"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_name, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {question}\n")
    print(f"DEBUG: Logged unanswered question: '{question}' to {log_file_name}") # For immediate feedback
# -----------------------------------------------

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
        },
        {
            "keywords": ["products", "offerings", "items", "stuff", "sell"],
            "answer": "We offer a wide range of authentic African fabrics, including Kente, Ankara, and Batik, as well as custom design services. What specifically are you interested in?"
        }
    ]

    # --- FUNCTION FOR GETTING RESPONSE ---
    def get_bot_response(user_question_processed, faqs):

        best_match_score = 0
        
        # NEW: List to store all good matches
        potential_matches = [] 

        MATCH_THRESHOLD = 80 
        # NEW: If other matches are within this score range of the best, ask for clarification
        CLARIFICATION_THRESHOLD = 10 

        # Iterate through each FAQ entry in our data
        for faq_entry in faqs:
            current_faq_max_score = 0 # To find the best score for THIS specific FAQ entry (reset for each faq_entry)

            # Check each keyword associated with the current FAQ entry
            for keyword in faq_entry["keywords"]:
                score = fuzz.partial_ratio(keyword, user_question_processed)

                # --- DEBUG PRINTS: CORRECTLY PLACED INSIDE THE INNER LOOP ---
                print(f"DEBUG: Comparing keyword '{keyword}' with user input '{user_question_processed}' -> Score: {score}")
                print(f"DEBUG: Current best_match_score before potential update: {best_match_score}")
                # -----------------------------------------------------------

                # Update the overall best_match_score found so far
                if score > best_match_score:
                    best_match_score = score

                # Update the max score for the current FAQ entry
                if score > current_faq_max_score: 
                    current_faq_max_score = score
            
            # After checking all keywords for the current faq_entry, if it's a good match, add it to potential_matches
            if current_faq_max_score >= MATCH_THRESHOLD:
                # Store the FAQ entry and its highest matching score
                potential_matches.append({
                    "faq_entry": faq_entry,
                    "score": current_faq_max_score
                })


        # --- DEBUG PRINT: After all loops have completed ---
        print(f"DEBUG: Final best_match_score: {best_match_score} (Threshold: {MATCH_THRESHOLD})") 
        # --------------------------------------------------

        # --- NEW LOGIC FOR DISAMBIGUATION ---
        
        # Filter potential_matches based on proximity to the best_match_score
        # Only consider matches that are very close to the highest score achieved
        top_contenders = [
            match_info for match_info in potential_matches
            if match_info["score"] >= (best_match_score - CLARIFICATION_THRESHOLD)
        ]

        # Decide the response based on the number of top contenders
        if len(top_contenders) == 1:
            # Only one clear best match, return its answer
            return top_contenders[0]["faq_entry"]["answer"]
        elif len(top_contenders) > 1:
            # Multiple strong contenders, ask for clarification
            # We'll use the first keyword as a simple label for clarification.
            # Convert to title case for better readability in the question.
            options = [entry["faq_entry"]["keywords"][0].replace("types of ", "").title() for entry in top_contenders] 
            
            # Formulate the clarification question nicely based on the number of options
            if len(options) == 2:
                clarification_question = f"It sounds like you might be asking about {options[0]} or {options[1]}? Could you please clarify?"
            else: # For 3 or more options
                clarification_question = f"It sounds like you might be asking about {', '.join(options[:-1])} or {options[-1]}? Could you please clarify?"
            return clarification_question
        else:
            # No strong matches found at all (best_match_score was below MATCH_THRESHOLD)
            log_unanswered_question(user_question_processed) 
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