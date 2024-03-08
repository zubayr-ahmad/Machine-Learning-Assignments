import googletrans as gt
import speech_recognition as sr
import gtts
import playsound as pls

# change the languages accordngly
input_lang = "en"
output_lang = "ur"

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak Now")
    try:
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio,language=input_lang)
        print(text)
    except Exception as e:
        print(e)
        print("Sorry, I could not recognize your voice")
        exit()

try:
    # print(gt.LANGUAGES)
    translator = gt.Translator()
    translation = translator.translate(text,dest=output_lang)
    print(translation.text)
    converted_audio = gtts.gTTS(translation.text,lang=output_lang)
    converted_audio.save("audio_file.mp3")
    pls.playsound("audio_file.mp3")
except Exception as e:
    print(e)
    print("Sorry, I could not translate your text")
    exit()