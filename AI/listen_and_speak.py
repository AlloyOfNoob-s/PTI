import pyttsx3
import speech_recognition
ear = speech_recognition.Recognizer()
def speak(text:str):
    speaker = pyttsx3.init()
    speaker.say(text)
    speaker.runAndWait()

def listen()->str:
    try:
        with speech_recognition.Microphone() as mic:
            print("successfully init microphone!")
            print(type(mic))
            user_input = ear.listen(mic,timeout=2,phrase_time_limit=2)
            text = ear.recognize_google(user_input)
            text = text.lower()
            return text
    except speech_recognition.UnknownValueError:
        return ""
    except speech_recognition.RequestError:
        return ""
print(listen())
