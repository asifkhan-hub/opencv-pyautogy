import speech_recognition as sr
import pyttsx3
import subprocess
import pyautogui

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_text_editor():
    # Specify the full path to "gedit" on Kali Linux
    subprocess.Popen(["/usr/bin/gedit"])

def type_text(text):
    pyautogui.write(text)

def save_text():
    pyautogui.hotkey('ctrl', 's')
    speak("File has been saved.")

def execute_command(command):
    if "open text editor" in command:
        open_text_editor()
        speak("Text editor is now open.")
    elif "type something" in command:
        text_to_type = "Hello, World! Have a nice day."  # Replace with your desired text
        type_text(text_to_type)
        speak("Text has been typed.")
    elif "save" in command:
        save_text()
    else:
        speak("I didn't understand that command.")

# Main loop
while True:
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print("You said: " + command)
            execute_command(command)
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
