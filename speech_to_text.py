import speech_recognition as sr

def transcribe_speech_input():
    """
    Listens for audio input from the user's microphone and transcribes it to text.
    Returns: The transcribed text (string) or an error message.
    """
    # Initialize the recognizer
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening for speech...")
        # Adjust for ambient noise for better accuracy
        r.adjust_for_ambient_noise(source, duration=0.5) 
        
        try:
            # Listen to the user's input
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            return "SpeechTimeoutError"
        except Exception:
             return "MicrophoneError"


    # Recognize speech using Google Speech Recognition
    try:
        # Use a reliable recognizer like Google's
        text_query = r.recognize_google(audio)
        print(f"Transcription: {text_query}")
        return text_query
        
    except sr.UnknownValueError:
        return "UnknownValueError"
    except sr.RequestError:
        return "ServiceUnavailable"