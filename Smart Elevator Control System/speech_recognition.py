import speech_recognition as sr

def run_speech_recognition():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Say something...")

        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("🧠 You said:", text)
            return text

        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None

        except sr.RequestError:
            print("❌ Speech service error")
            return None