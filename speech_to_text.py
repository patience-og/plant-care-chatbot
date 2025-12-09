import speech_recognition as sr
import time

# Function name MUST match the import in app.py
def get_voice_input(api_choice, language_code):
    """
    Listens for audio input and transcribes it using the selected API and language.
    Returns: A tuple (status_code, text_or_error_message).
    """
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening for speech...")
        
        # Adjust for ambient noise for better accuracy
        r.adjust_for_ambient_noise(source, duration=0.5) 

        try:
            # Listen to the user's input with a 5-second timeout
            # Note: phrase_time_limit prevents listening indefinitely after speech stops
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            # Status 408: No speech detected
            return 408, "No speech detected within 5 seconds."
        except Exception:
            # Status 500: General mic/hardware error
            return 500, "Microphone hardware error. Ensure it's connected and permissions are granted."

    # --- Speech Recognition APIs ---
    try:
        if api_choice == "Google Speech Recognition":
            text_query = r.recognize_google(audio, language=language_code)
        
        elif api_choice == "Sphinx (Offline)":
            # Note: Sphinx is complex and may require additional local files/dependencies
            text_query = r.recognize_sphinx(audio, language=language_code)
        
        else:
            return 400, "Selected API is not supported or misconfigured."
            
        print(f"Transcription: {text_query}")
        # Status 200: Success
        return 200, text_query

    except sr.UnknownValueError:
        # Status 400: Audio not understood
        return 400, "Could not understand audio. Please speak clearly or try a different language setting."
    except sr.RequestError as e:
        # Status 503: API or Network Error (happens if Google service is unreachable)
        return 503, f"Could not request results from {api_choice} service; check network connection. Error: {e}"
    except Exception as e:
        # Catch any other unexpected errors
        return 500, f"An unexpected error occurred during transcription: {e}"