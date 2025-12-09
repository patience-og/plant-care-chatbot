import streamlit as st
# Assuming your chatbot logic is in chatbot.py
from chatbot import plant_chatbot 
# Import the new speech transcription function
from speech_to_text import transcribe_speech_input 


# --- Configuration ---
st.set_page_config(page_title="🗣️ Voice-Enabled Plant Chatbot", page_icon="🌱", layout="centered")

st.title("🗣️ Voice-Enabled Plant Care Helper")
st.markdown("You can ask questions via **text** or by clicking the **🎙️ Speak** button.")
st.markdown("---")

# Initialize session state for text input so we can update it from speech
if 'text_query' not in st.session_state:
    st.session_state.text_query = ""

# --- A. Speech Input Section ---

st.header("1. 🎙️ Voice Input")

if st.button("Click to Speak and Ask"):
    # Clear previous text input to show voice transcription result clearly
    st.session_state.text_query = ""
    st.session_state.app_ran = True

    with st.spinner('Listening... Speak now!'):
        # Call the speech transcription function
        transcribed_text = transcribe_speech_input()

    # Handle errors and update the text box
    if transcribed_text == "SpeechTimeoutError":
        st.error("No speech detected. Please try again.")
    elif transcribed_text == "UnknownValueError":
        st.warning("Could not understand audio. Please speak clearly.")
    elif transcribed_text == "ServiceUnavailable":
        st.error("Speech recognition service unavailable. Check internet connection.")
    elif transcribed_text == "MicrophoneError":
        st.error("Microphone error. Ensure PyAudio and a microphone are working.")
    else:
        # Success: Update the text input box with the transcribed text
        st.session_state.text_query = transcribed_text
        st.success(f"Transcribed Text: **{transcribed_text}**")


# --- B. Text Input Section ---

st.header("2. 💬 Text Input")

# Use a key to link the text input to the session state variable
user_input = st.text_input(
    "Type your question:", 
    key='user_input_key', 
    value=st.session_state.text_query, # Initializes with transcribed speech or previous input
    placeholder="e.g., How often should I water my Aloe Vera?"
)


# --- C. Chatbot Response Section ---


if user_input and user_input != st.session_state.text_query:
    # Run the chatbot only if the input was manually typed
    run_chatbot = True
elif 'app_ran' in st.session_state and st.session_state.app_ran and user_input == st.session_state.text_query:
    # Run the chatbot if the input was from a successful speech transcription
    run_chatbot = True
else:
    run_chatbot = False

if run_chatbot:
    with st.spinner('Generating response...'):
        response = plant_chatbot(user_input)
        
    st.markdown("---")
    st.markdown("### 💡 Chatbot Response:")
    st.write(response)

st.markdown("---")
st.caption("Chatbot powered by TF-IDF and Streamlit.")