import streamlit as st
# Make sure your main logic file is named 'chatbot.py'
from chatbot import plant_chatbot 

st.set_page_config(page_title="🌿 Plant Care Helper", page_icon="🌱", layout="centered")

st.title("🌿 Plant Care Helper Chatbot")
st.markdown("Ask about **Kenyan & Meru local plants**, indoor plants, or flowers!")

st.markdown("---")

user_input = st.text_input("🌱 What is your question about plant care?", 
                           placeholder="e.g., How often should I water my Spider Plant?")

if user_input:
    # Use a spinner while the chatbot processes the query
    with st.spinner('Thinking... Searching plant knowledge base...'):
        try:
            # Call the main chatbot function
            response = plant_chatbot(user_input)
            
            # Display the response
            st.markdown("### 💡 Recommended Answer:")
            # st.write uses markdown automatically, which is needed for the \n\n breaks
            st.write(response)
            
        except Exception as e:
            # Use this to catch any unexpected errors (like missing libraries)
            st.error(f"❌ An error occurred during processing: {e}")

st.markdown("---")
st.caption("This chatbot uses TF-IDF similarity to match your question to information in the `plant.txt` file.")

