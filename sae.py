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
import curses
import locale
import socket
from gtts import gTTS
from TTS.api import TTS
from ctypes import *
from pydub import AudioSegment
from sklearn.neural_network import MLPClassifier
from vosk import SetLogLevel, Model, KaldiRecognizer
from io import BytesIO
from time import sleep
from sys import argv, stdout
from subprocess import Popen, PIPE

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

def speak(str, w1, lang):
    if not str: return
    w1.writeln(f"SAE: {str}")
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith('127.0.'):
        f = BytesIO()
        noecho();tts.tts_to_file(text=str, file_path=f);echo()
    else:
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

def ssh(w1):
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith('127.0.'):
        speak("No puedo iniciar SSH, necesito conectarme a internet.", w1, lang='es')
        return
    pr = Popen(("systemctl", "status", "sshd"), stdout=PIPE, stderr=PIPE)
    pr.wait()
    if pr.returncode:
        pr = Popen(("sudo", "systemctl", "start", "sshd"), stdout=PIPE, stderr=PIPE)
        pr.wait()
    speak(f"Listo, ya inicié ssh, mi IP es {ip}", w1, lang='es')

def ip(w1):
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith('127.0.'):
        speak("No estoy conectada a la red, así que no tengo una IP disponible.", w1, lang='es')
    else:
        speak(f"Tu IP es {ip}", w1, lang='es')

def wifi(w1):
    pr = Popen(("sudo", "wificreds"), stdout=PIPE, stderr=PIPE)
    pr.wait()
    if pr.returncode == 1:
        speak("No he podido conectarme a la red, no tengo permisos suficientes.", w1, lang="es")
    elif pr.returncode == 2:
        speak("No he podido conectarme a la red, el archivo WiFi en la USB tiene un formato incorrecto. No podré usarlo.", w1, lang="es")
    else:
        if socket.gethostbyname(socket.gethostname()).startswith('127.0.'):
            speak("Ocurrió un error. No puedo conectarme a la red.", w1, lang="es")
        else:
            speak("Listo, ya estoy en línea", w1, lang="es")

def quit(w1):
    speak("Hasta luego", w1, lang="es");exit(0)

ANS = {
        "hola": [None,"Hola! Cómo estás?"],
        "hola sae": [None, "Hola! Cómo estás?"],
        "chau": [quit, ""],
        "chao": [quit, ""],
        "chau, sae": [quit, ""],
        "adiós": [quit, ""],
        "conéctate a wi-fi": [wifi, "Claro, dame un momento"],
        "activa el acceso remoto": [ssh, "Claro, dame un momento"],
        "cual es tu direccion": [ip, ""]
        }

EMO = json.load(open("emotion.json"))

class Winbuff:
    def __init__(self, win, buff=""):
        self.win = win
        self.buff = buff
    def write(self, str):
        self.buff += str
        self.win.addstr(str)
        self.win.refresh()
    def writeln(self, str): self.write(str+'\n')
    def eraseline(self): 
        self.buff = self.buff[:self.buff.strip().rfind('\n')]
        self.win.move(self.win.getyx()[0], 0);self.win.clrtoeol()
    def clear(self): self.buff = ""
    def dump(self):
        self.win.addstr(self.buff)
        self.win.refresh()

def redraw(stdscr, f1="", f2=""):
    stdscr.move(0,0); stdscr.clrtobot()
    y,x = stdscr.getmaxyx()
    COLS = (y-4-1)//2
    b1 = curses.newwin(COLS+1, x-2-1, 0, 1)
    b2 = curses.newwin(COLS+1, x-2-1, COLS+2, 1)
    w1 = curses.newwin(COLS-1, x-5, 1, 2); w1.scrollok(1)
    w2 = curses.newwin(COLS-1, x-5, COLS+3, 2); w2.scrollok(1)
    b1.box(curses.ACS_VLINE, curses.ACS_HLINE)
    b2.box(curses.ACS_VLINE, curses.ACS_HLINE)
    stdscr.refresh()
    b1.refresh(); b2.refresh()
    w1.refresh(); w2.refresh()
    a = Winbuff(w1, f1);a.dump()
    b = Winbuff(w2, f2);b.dump()
    return a,b

def main(stdscr):
    locale.setlocale(locale.LC_ALL, "")
    curses.start_color()
    curses.curs_set(0)
    curses.noecho()
    curses.init_pair(1, 1, 0)
    curses.init_pair(2, 2, 0)
    curses.init_pair(3, 3, 0)
    curses.init_pair(4, 4, 0)
    curses.init_pair(11, 0, 1)
    curses.init_pair(12, 0, 2)
    curses.init_pair(13, 0, 3)
    curses.init_pair(14, 0, 4)
    np.seterr(all='ignore')
    w1,w2 = redraw(stdscr)
    w2.write("Iniciando Serial..")
    srl = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
    curses.napms(2000)
    w2.writeln("OK")
    w2.write("Cargando modelo...")
    F = open('neural_network/mlp_classifier.model-all', 'rb')
    model = pickle.load(F)
    w2.writeln("OK")

    w2.write("Ajustando parámetros..")
    noecho()
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source: r.adjust_for_ambient_noise(source)
    echo()
    w2.writeln(f"OK")
    
    speak("Ya estoy lista para escuchar", w1, lang='es')
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
            w2.write("Micrófono ");w2.win.addstr(" ", curses.color_pair(12));w2.win.refresh()
            noecho()
            with m as source: audio = r.listen(m)
            echo()
            faudio = BytesIO(audio.get_wav_data())
            w2.eraseline()
            w2.write("Micrófono ");w2.win.addstr(" ", curses.color_pair(11));w2.win.refresh()
            features = extract_feature(faudio, mfcc=True, chroma=True, mel=True)
            x = model.predict(features)[0]
            emotion = emotospanish(x)
            send((x+'\n').encode('utf-8'))
            try:
                if socket.gethostbyname(socket.gethostname()).startswith('127.0.'):
                    wav = BytesIO(audio.get_wav_data())
                    wav = wave.open(wav, 'rb')
                    vmodel = Model(lang='es')
                    rec = KaldiRecognizer(vmodel, wav.getframerate())
                    rec.SetWords(True)
                    rec.SetPartialWords(True)
                    while True:
                        data = wav.readframes(4000)
                        if not len(data): break
                        rec.AcceptWaveform(data)
                    result = json.loads(rec.FinalResult())['text'].lower()
                else:
                    value = r.recognize_google(audio, language='es-ES', show_all=True)
                    result = value['alternative'][0]['transcript'].lower()
                w1.writeln(f"Tú ({x}): {result}")
                if ANS.get(result):
                    obj = ANS.get(result)
                    speak(obj[1], w1, lang="es")
                    if obj[0]: obj[0](w1)
                else:
                    speak(EMO[x], w1, lang="es")
            except sr.UnknownValueError:
                w2.eraseline()
                continue
            except sr.RequestError:
                speak("No estoy pudiendo reconocer lo que dices, ¿Estoy conectada a internet?", w1, lang='es')
                continue
            except Exception:
                w2.eraseline()
                continue
            w2.eraseline()
    
if __name__ == "__main__":
    SetLogLevel(-1)
    noecho();tts = TTS(TTS.list_models()[22]);echo()
    curses.wrapper(main)

