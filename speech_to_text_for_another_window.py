import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Define the function to listen for voice commands
def listen_for_command():
    print("Слухаю...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize the speech using Google Speech Recognition with Ukrainian language
        command = recognizer.recognize_google(audio, language="uk-UA").lower()
        print(f"Результат: {command}")

    except sr.UnknownValueError:
        print("Розпізнавання мови не вдалося.")
    except sr.RequestError as e:
        print(f"Не вдалося отримати результати від служби Google Speech Recognition; {e}")

# Call the function to listen for voice commands
listen_for_command()
