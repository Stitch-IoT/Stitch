import speech_recognition as sr

def start_program():
    print("Програма розпочалася!")  # Print a message in Ukrainian

# Initialize the recognizer
recognizer = sr.Recognizer()
trigger_words = ["перепрошую", "ігор", "обережно", "увага"]

# Define the function to listen for voice commands
def listen_for_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize the speech using Google Speech Recognition with Ukrainian language
        command = recognizer.recognize_google(audio, language="uk-UA").lower()
        print(f"Отримано команду: {command}")

        # Check if any trigger word is present in the command
        if any(word in command for word in trigger_words):
            start_program()
            return True  # Return True to indicate that the function has been executed
        
        else:
            print("Команда не визначена.")

    except sr.UnknownValueError:
        print("Розпізнавання мови не вдалося.")
    except sr.RequestError as e:
        print(f"Не вдалося отримати результати від служби Google Speech Recognition; {e}")

# Continuously listen for commands
while True:
    if listen_for_command():
        break  # Exit the loop if start_program() is executed
