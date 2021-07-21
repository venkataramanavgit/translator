import os

from flask import Flask, render_template, make_response, request
import googletrans
import speech_recognition as sr
import gtts
import playsound

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('hello.html')

@app.route('/trans/')
def my_link():
  print ('I got clicked!')
  if os.path.exists('./static/anylang1.mp3') :
      os.remove('./static/anylang1.mp3')
  if os.path.exists('./static/anylang.mp3') :
      os.remove('./static/anylang.mp3')
  return render_template('trans.html')

@app.route('/speak/', methods=['POST'])
def speak():

    opt = request.form.get('op')
    recognizer = sr.Recognizer()
    translator = googletrans.Translator()
    text=''
    try:
        with sr.Microphone() as source:
            print(' can speak now')
            recognizer.adjust_for_ambient_noise(source=source)
            voice = recognizer.listen(source, timeout=0.5)
            print('processing')
            text = recognizer.recognize_google(voice)
    except:
        pass
    outp = gtts.gTTS(text, lang='en')
    outp.save(os.path.join(app.root_path, 'static','anylang1.mp3'))
    translated = translator.translate(text, dest=opt)

    converted_audio = gtts.gTTS(translated.text, lang=opt)
    converted_audio.save(os.path.join(app.root_path, 'static','anylang.mp3'))



    return render_template('trans.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81,debug=True)


