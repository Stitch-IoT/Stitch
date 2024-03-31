from gtts import gTTS
def text_to_speach(text):
    language = "uk"
    speach = gTTS(text=text, lang=language, slow=False, tld="co.uk")
    file = "text.mp3"
    speach.save(file)
    return file