import streamlit as st
import time
# Import the core chatbot logic
from chatbot import plant_chatbot 
# Import the voice transcription function (renamed for stability)
from speech_to_text import get_voice_input 

# --- CONFIGURATION ---
API_OPTIONS = ["Google Speech Recognition", "Sphinx (Offline)"]
LANGUAGE_OPTIONS = {
    "English (US)": "en-US",
    "Swahili (Tanzania)": "sw-TZ",
    "Spanish (Spain)": "es-ES",
    "French (France)": "fr-FR"
}

# --- SESSION STATE INITIALIZATION ---
if 'text_query' not in st.session_state:
    st.session_state.text_query = ""
if 'is_paused' not in st.session_state:
    st.session_state.is_paused = False
if 'saved_text' not in st.session_state:
    st.session_state.saved_text = ""

def toggle_pause():
    """Toggles the pause state for the microphone."""
    st.session_state.is_paused = not st.session_state.is_paused

def save_transcribed_text():
    """Saves the current transcribed text to session state for download."""
    if st.session_state.text_query:
        st.session_state.saved_text = st.session_state.text_query
        st.success("Text saved locally. Use the Download button to save to a file.")
    else:
        st.warning("Nothing to save yet. Speak or type first.")

# --- STREAMLIT UI LAYOUT ---

st.set_page_config(page_title="🗣️ Voice-Enabled Plant Chatbot", page_icon="🌱", layout="centered")

st.title("🌱 Voice-Enabled Plant Care Helper")
st.markdown("Ask questions about plant care using your **voice** or **text** input.")
st.markdown("---")

## ⚙️ Settings and Controls
st.header("1. Settings & Controls")
col1, col2, col3 = st.columns(3)

with col1:
    api_choice = st.selectbox("Speech API", API_OPTIONS)

with col2:
    lang_display = st.selectbox("Language", list(LANGUAGE_OPTIONS.keys()))
    language_code = LANGUAGE_OPTIONS[lang_display]

with col3:
    # Pause/Resume Feature
    button_label = "Resume Listening" if st.session_state.is_paused else "Pause Listening"
    st.button(button_label, on_click=toggle_pause)


## 🎙️ Voice Input Section
st.subheader("Start Conversation")

if st.session_state.is_paused:
    st.warning("Listening is currently paused. Click 'Resume Listening' above to use your microphone.")
else:
    if st.button("Click to Speak and Ask 🎙️"):
        # Clear previous input and set flag for immediate chatbot run
        st.session_state.last_run_query = ""
        st.session_state.text_query = "" 

        # Run transcription only if not paused
        with st.spinner(f'Listening for {lang_display}... Speak clearly now!'):
            # Call the renamed function
            status, text_result = get_voice_input(api_choice, language_code)

        # Handle transcription results
        if status == 200:
            st.session_state.text_query = text_result
            # Set the query for immediate chatbot run
            st.session_state.last_run_query = text_result
            st.success(f"Transcribed Text: **{text_result}**")
        elif status == 400:
            st.warning(f"Transcription Error: {text_result}")
        else:
            st.error(f"Hardware/Network Error: {text_result}")


## 💬 Text Input and Save Feature
st.header("2. Question and Actions")

# Text Input box (takes transcribed text or manual input)
user_input = st.text_input(
    "Final Question (Type or Speak):", 
    key='user_input_key', 
    value=st.session_state.text_query,
    placeholder="Enter your question or use voice input..."
)

col_save, col_download = st.columns(2)
with col_save:
    st.button("Save Transcribed Text", on_click=save_transcribed_text)

# Download Button (only appears after 'Save Text' is clicked and there's content)
if st.session_state.saved_text:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"transcribed_text_{timestamp}.txt"
    with col_download:
        st.download_button(
            label="Download Text File 💾",
            data=st.session_state.saved_text,
            file_name=filename,
            mime="text/plain"
        )

## 💡 Chatbot Response Section

# Check if the current input is new (either manual change OR just received from voice)
if user_input and user_input != st.session_state.get('last_run_query', ''):
    st.session_state.last_run_query = user_input # Update the last run query
    
    with st.spinner('Generating chatbot response...'):
        response = plant_chatbot(user_input)
        
    st.markdown("---")
    st.markdown("### 💡 Chatbot Response:")
    # st.write handles the \n\n formatting from chatbot.py
    st.write(response)

st.markdown("---")
st.caption("Chatbot powered by TF-IDF and Streamlit.")