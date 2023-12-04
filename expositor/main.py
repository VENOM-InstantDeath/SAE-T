import soundfile as sf
import sounddevice as sd
import serial
import os
from pydub import AudioSegment
from gpiozero import Button
from signal import pause
from time import sleep

C=0
AUDIO=[]
SRL = serial.Serial(port='/dev/ttyACM0', baudrate=9600)

def play(s):
    print("Button was pressed!!")
    global C
    if C == len(AUDIO):
        C = 0
        return
    s.write(b'next\n')
    sd.play(AUDIO[C]['data'], AUDIO[C]['fs'])
    sd.wait()
    C+=1

def main():
    print("Program started")
    l=os.listdir('audio');l.sort()
    bt = Button(26)
    print("Button detected")
    for i in sorted(os.listdir('audio')):
        data,fs=sf.read(f'audio/{i}', dtype='float32')
        AUDIO.append({'data': data, 'fs': fs})
    print("Ready")
    with SRL as s:
        if bt.is_pressed: play(s)
        sleep(0.2)

if __name__=='__main__':
    main()
