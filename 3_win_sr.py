import speech_recognition as sr

def recognize_speech(device_index):
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Capture audio from the specified microphone
    with sr.Microphone(device_index=device_index) as source:
        print("Please say something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio_data = recognizer.listen(source)  # Listen for speech

    try:
        # Recognize speech using Google Speech Recognition
        recognized_text = recognizer.recognize_google(audio_data)
        return recognized_text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print("Error occurred; {0}".format(e))

def main():
    # Specify the device index of the microphone you want to use
    # You can find the index of available microphones using the following code:
    # for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #     print("Microphone with index {0} : {1}".format(index, name))
    # Choose the index corresponding to your desired microphone
    device_index = 1  # Change this to the index of your desired microphone

    # Call the speech recognition function with the specified device index
    recognized_text = recognize_speech(device_index)

    # Print the recognized text
    print("You said:", recognized_text)

if __name__ == "__main__":
    main()
