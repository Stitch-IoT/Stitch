from gtts import gTTS
def text_to_speech(text):
    language = "uk"
    speach = gTTS(text=text, lang=language, slow=False, tld="co.uk")
    file = "asserts/voice.mp3"
    speach.save(file)
    return file