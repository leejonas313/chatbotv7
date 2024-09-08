import re
import streamlit as st
import pandas as pd

# Load dataset from Excel file
def load_dataset(file_path):
    df = pd.read_excel(file_path)
    return df

# Load the dataset from the correct file
procurement_data = load_dataset(r'C:\Users\USER\Desktop\aiassignment\chatbot_dataset.xlsx')


# Function to find the best match from the dataset
def find_best_match(user_message, dataset):
    for index, row in dataset.iterrows():
        keywords = row['Keywords'].split(',')  # Assuming 'Keywords' column
        if any(word in user_message for word in keywords):
            return row['Response']  # Assuming 'Response' column
    return None

# Function to handle message probability (can remain unchanged)
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

# Check all messages and determine the best response
def check_all_messages(message, dataset):
    best_match = find_best_match(message, dataset)
    return best_match if best_match else unknown()

# Function for unknown responses
def unknown():
    response = ["I'm not sure I understand. Can you ask about procurement?",
                "I couldn't catch that. Please try rephrasing.",
                "I'm not sure what you're asking. Do you need help with procurement?",
                "That doesn't seem related to procurement. Can you clarify?"][
        random.randrange(4)]
    return response

# Function to get chatbot response
def get_response(user_input, dataset):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message, dataset)
    return response

# Streamlit App
def main():
    st.title("Procurement Chatbot")
    st.write("Ask me anything about the procurement process!")

    user_input = st.text_input("You:", "")

    if st.button("Send"):
        if user_input.strip() != "":
            bot_response = get_response(user_input, procurement_data)
            st.text_area("Bot:", bot_response, height=150)
        else:
            st.warning("Please enter a message.")

if __name__ == '__main__':
    main()
