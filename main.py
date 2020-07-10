# importiamo la libreria per il riconoscimento vocale
import speech_recognition as sr
# Ci permette di utilizare il nostro browser web
import webbrowser
from time import ctime
# Lo usiamo per far ascoltare il microfono senza che finisca con una sola domanda
import time
# importiamo la libreria per riprodure il suono che l'assistente produrrà
import playsound
# importiamo il pacchetto core di python
import os
# importiamo la libreria random, perchè vogliamo generare un nome random per il file per la risposta di google
import random
# importiamo il google text speech, per poter parlare con noi
from gtts import gTTS

import datetime
import calendar
import locale

import urllib.request
import urllib.parse
import re

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


import ast
import math

# for Romanian locale
locale.setlocale(locale.LC_TIME, "ro_RO")

# Inizializiamo il riconoscitore, e responsabile per il riconoscimento del discorso vocale
r = sr.Recognizer()


# google creera un file, che dopo dovremmo riprodurre. Quindi per ogni risposta verrà creato un file .mp3
# usando la libreria os possiamo eliminare questi file, per far si che non si accumulino


class person:
    name = ''
    age = ''

    def setName(self, name):
        self.name = name

    def setAge(self, age):
        self.age = age


class asis:
    name = ''
    age = ''

    def setName(self, name):
        self.name = name

    def setAge(self, age):
        self.age = age


# Creaimo un metodo per cercare nelle parole con lo stesso significato,
# in modo tale da far capire Ioana cosa vogliamo dire
def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True


# Definiamo una funzione
# avremo un parametro ask che e optionale, per questo e messo su false
def record_audio(ask=False):
    # Utiliziamo il microfono, quindi la fonte sarà il nostro microfono
    with sr.Microphone() as source:
        # se esiste una domanda
        if ask:
            # facciamo dire all'assistente la domanda
            assistant_speak(ask)
        # Ascolta la prima frase ed estraila nella variabile audio
        audio = r.listen(source)
        voice_data = ''
        try:
            # Variabile che conterrà ciò che diremo al microfono
            # Lo utiliziamo perchè ci transcrive in stringa ciò che ha sentito al microfono,
            # in questo caso nella variabile audio
            # il cui contiene il nostro audio e lo trasformerà in testo
            # language indica che google deve capire l'audio in Rumeno
            voice_data = r.recognize_google(audio, language="ro")
        except sr.UnknownValueError:
            assistant_speak("Imi pare rau dar nu am inteles")
        except sr.RequestError:
            assistant_speak("Iartama dar serviciul meu vocal nu merge momentan")
        return voice_data


# Creaimo una funzione per far parlare l'assistente vocale
def assistant_speak(audio_string):
    # creiamo una variabile che conterrà il testo letto da google translate nella lingua rumena
    tts = gTTS(text=audio_string, lang='ro')
    # generiamo un numero random per poi assegnarlo come nome del file audio che si genererà
    r = random.randint(1, 10000000)
    # creiamo il nome dell'audio file
    # str() viene usato per convertire un numero in stringa
    audio_file = 'audio-' + str(r) + '.mp3'
    # salviamo il file audio
    tts.save(audio_file)
    # voglio che lo riproduca subito
    playsound.playsound(audio_file)
    # stampiamo ciò che l'assistente dice
    print(audio_string)
    # rimuoviamo il file
    os.remove(audio_file)


# Creo una funcione per la risposta ai nostri dati
def respond_data(voice_data):
    # Se la frase dentro '' e presente nel voice_data
    if 'Cum te numești' in voice_data:
        assistant_speak("Numele meu este " + assistant_obj.name)
        user_name = record_audio('Care este numele tău?')
        person_obj.setName(user_name)
        assistant_speak("Ok, mulțumesc " + person_obj.name)

    if 'Cât e ceasul' in voice_data:
        now = datetime.datetime.now()
        assistant_speak(str(now.hour) + ' și ' + str(now.minute) + 'minute')

    if there_exists(['În ce zi suntem azi', 'ce zi e azi', 'Ce zi e azi']):
        now = datetime.datetime.now()
        assistant_speak('Astazi suntem in ' + str(now.day) + calendar.month_name[now.month])

    if there_exists(['mă iubești']):
        if person_obj.name == 'Antonio':
            assistant_speak("Normal că te iubesc iubire, eu trăiesc doar pentru tine")
        else:
            assistant_speak("Nu, eu il iubesc doar pe Antonio")

    if there_exists(['caută', 'cauta']):
        # creo una variabile che conterà il nostro nuovo audio, per far sapere cosa voglio cercare
        # quindi in pratica diremo 2 cose: 1 search e dopo 2. cosa vogliamo cercare
        # Il risultato di quello che diaciamo al microfono lo conterrà quata variabile search
        search = record_audio('Ce vrei sa caut?')
        # Creaimo url per google
        url = 'https://google.com/search?q=' + search
        # Facciamo aprire il broser sul url scritto sopra
        webbrowser.get().open(url)
        assistant_speak("Aste este ce am gasit pentru " + search)

    if there_exists(['ce vârstă ai', 'câți ani ai']):
        assistant_speak("Varsta mea este de " + assistant_obj.age)

    if there_exists(['de acuma te numești', 'numele tău este']):
        assistant_name = voice_data.split()[-1].strip()
        assistant_obj.setName(assistant_name)
        assistant_speak("Ok, de acuma numele meu este " + assistant_obj.name)

    if there_exists(["Caută pe YouTube"]):
        search_term = record_audio('Ce anume vrei sa caut pe youtube?')
        print(search_term)
        # song name from user
        song = urllib.parse.urlencode({"search_query": search_term})
        print(song)

        # fetch the ?v=query_string
        result = urllib.request.urlopen("https://www.youtube.com/results?" + song)
        print(result)

        # make the url of the first result song
        search_results = re.findall(r'\/watch\?v=(.{11})', result.read().decode())
        print(search_results)

        # make the final url of song selects the very first result from youtube result
        url = "https://www.youtube.com/watch?v=" + search_results[0]

        # play the song using webBrowser module which opens the browser
        # webbrowser.open(url, new = 1)
        webbrowser.open_new(url)
        assistant_speak("Asta e ce am gasit pe youtube " +
                        search_term)
        exit()

    if there_exists(['Cât face', 'cat face']):
        first_number = voice_data.split()[-3].strip()
        second_number = voice_data.split()[-1].strip()
        operator = voice_data.split()[-2].strip()

        if operator == 'plus':
            assistant_speak('Resultatul este ' + str(ast.literal_eval(first_number) + ast.literal_eval(second_number)))
        elif operator == 'minus':
            assistant_speak('Resultatul este ' + str(ast.literal_eval(first_number) - ast.literal_eval(second_number)))
        elif operator == 'ori':
            assistant_speak('Resultatul este ' + str(ast.literal_eval(first_number) * ast.literal_eval(second_number)))
        elif operator == 'împărțit':
            assistant_speak('Resultatul este ' + str(ast.literal_eval(first_number) / ast.literal_eval(second_number)))
        elif operator == 'puterea':
            assistant_speak('Resultatul este ' + str(ast.literal_eval(first_number) ** ast.literal_eval(second_number)))

    if there_exists(['pa', 'trebuie sa ies', 'ne auzim']):
        assistant_speak("Ok, ai grija de tine")
        exit()


assistant_obj = asis()
person_obj = person()

assistant_obj.setName('Ioana')
assistant_obj.setAge('18')

# aggiungiamo un tempo per continuare l'ascolto, senza che finisca dopo aver ottenuto la risposta ad una sola domanda
# Vogliamo continuare ad ascoltare
# aspetta per 1 secondo
time.sleep(1)

while 1:
    # Creiamo una variabile che avrà il risultato della funzione record_audio (in cui verrà registrato il nostro audio)
    # ha i nostri dati vocali (ciò che noi diciamo)
    voice_data = record_audio("Ascult")
    print("Done")
    print("Q:", voice_data)
    # Richiamo il metodo per la risposta
    respond_data(voice_data)
