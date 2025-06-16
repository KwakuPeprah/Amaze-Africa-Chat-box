# chatbot.py (Updated Version - Step 4)

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
        
        # Iterate through each FAQ entry in our data
        for faq_entry in faqs:
            # Check each keyword associated with the current FAQ entry
            for keyword in faq_entry["keywords"]:
                if keyword in user_question_processed:
                    return faq_entry["answer"] # Return the answer if a keyword matches

        # If no keyword matched from any FAQ
        return "I'm sorry, I don't understand your question. Could you please rephrase or ask about common topics like hours, designs, fabric types, location, or contact?"
    # --- END NEW FUNCTION ---


    while True:
        user_input = input("You: ")
        processed_input = user_input.lower()

        if processed_input == 'bye':
            print("Bot: Thank you for visiting Ama's Amazing African Fabrics. Goodbye!")
            break

        # Call our new function to get the bot's response
        response = get_bot_response(processed_input, faq_data)
        print(f"Bot: {response}")

if __name__ == "__main__":
    run_chatbot()