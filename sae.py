import pickle
import numpy as np
import wave
import soundfile
import librosa
import speech_recognition as sr
import os
import json
import serial
import soundfile as sf
import sounddevice as sd
from gtts import gTTS
from ctypes import *
from pydub import AudioSegment
from sklearn.neural_network import MLPClassifier
from io import BytesIO
from time import sleep
from sys import argv

GREEN = '\033[1;32m'; NM = '\033[0m'
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt): pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

fd = os.open("/dev/null", os.O_WRONLY)
os.dup2(1,fd+1)
os.dup2(2,fd+2)
def noecho():
    os.dup2(fd,1);os.dup2(fd,2)
def echo():
    os.dup2(fd+1,1);os.dup2(fd+2,2)

def emotospanish(str):
    d = {
            "Anger": "enojado",
            "Sadness": "triste",
            "Disgust": "disgustado",
            "Fear": "atemorizado",
            "Neutral": "neutral",
            "Happiness": "alegre"
        }
    return d[str]

def speak(str, lang):
    if not str: return
    x=gTTS(str, lang=lang)
    f=BytesIO(list(x.stream())[0])
    AudioSegment.from_mp3(f).export(f, format="wav")
    data,fs=sf.read(f, dtype='float32')
    sd.play(data,fs)
    sd.wait()
    f.close()

def extract_feature(file_name, **kwargs):
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)
            result = np.hstack((result, mel))
        if contrast:
            contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
            result = np.hstack((result, contrast))
        if tonnetz:
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
            result = np.hstack((result, tonnetz))
    return result.reshape(1,-1)

print("Iniciando Serial..",end='')
srl = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
sleep(2)
print(f"{GREEN}OK{NM}")
np.seterr(all='ignore')
print("Cargando modelo...", end="")
F = open('neural_network/mlp_classifier.model-all', 'rb')
model = pickle.load(F)
print(f"{GREEN}OK{NM}")

print("Ajustando parámetros..", end="")
noecho()
r = sr.Recognizer()
m = sr.Microphone()
with m as source: r.adjust_for_ambient_noise(source)
echo()
print(f"{GREEN}OK{NM}")

speak("Ya estoy lista para escuchar", lang='es')
with srl as s:
    def send(b):
        s.write(b)
    def receive():
        str = b''
        while True:
            r = s.read(1)
            if r == b'\n': return str.strip()
            str += r
    while True:
        print("Grabando del micrófono..")
        noecho()
        with m as source: audio = r.listen(m)
        echo()
        print(f"{GREEN}OK{NM}")
        faudio = BytesIO(audio.get_wav_data())
        print("Procesando..", end="")  # Dijiste algo
        features = extract_feature(faudio, mfcc=True, chroma=True, mel=True)
        print(f"{GREEN}OK{NM}")
        print("Prediciendo emociones..")  # Reconociendo emoción
        x = model.predict(features)[0]
        emotion = emotospanish(x)
        send((x+'\n').encode('utf-8'))
        print(f"Predicción: {emotion}")
        speak(f"Te he escuchado. Sonaste {emotion}", lang='es')
        # Descomentar esto para reconocimiento de palabras
        #try:
        #    value = r.recognize_google(audio, language='es-ES', show_all=True)
        #    result = value['alternative'][0]['transcript']
        #except sr.UnknownValueError: continue
        #except sr.RequestError:
        #    speak("No estoy pudiendo reconocer lo que dices, ¿Estoy conectada a internet?", lang='es')
        #    continue
        #except Exception: continue


"""
Emociones = [
    "Anger",
    "Sadness",
    "Disgust",
    "Fear",
    "Neutral",
    "Happiness"
]
"""
