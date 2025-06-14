def run_chatbox():
    print("----------------------------------------")
    print("Hello! Welcome to Amaze Africa Fabrics")
    print("I can answer common questions. Type 'bye' to exit")
    print("----------------------------------------")

    while True: #This loop will run until the user types 'bye'
        user_input = input("You: ")

        if user_input.lower() == 'bye':
            print("Bot: thank you for visiting Amaze Africa Fabrics. Goodbye!")
            break #Exit the loop

        print(f"Bot: You asked: '{user_input}'.")

if __name__ == "__main__":
        run_chatbox()