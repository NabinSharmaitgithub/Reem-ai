def listen():
    """
    Listens to the microphone and returns the recognized text.
    """
    try:
        import speech_recognition as sr
    except ImportError:
        return "Error: speech_recognition not installed."

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening for command...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            print("Processing voice...")
            try:
                # Attempting offline recognition
                text = recognizer.recognize_sphinx(audio)
            except (sr.UnknownValueError, AttributeError, ImportError):
                return "Error: Offline speech recognition (pocketsphinx) not installed or could not understand."

            return text
    except Exception as e:
        return f"Error in voice module: {str(e)}"

if __name__ == "__main__":
    print("Voice module loaded.")
