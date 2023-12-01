import soundfile as sf
import sounddevice as sd
import os
from pydub import AudioSegment
from gpiozero import Button
from signal import pause

C=0
AUDIO=[]
def play():
    global C
    sd.play(AUDIO[C]['data'], AUDIO[C]['fs'])
    sd.wait()
    C+=1

def main():
    AUDIO = []
    l=os.listdir('audio');l.sort()
    bt = Button(26)
    for i in sorted(os.listdir('audio')):
        data,fs=sf.read(f'audio/{i}', dtype='float32')
        AUDIO.append({'data': data, 'fs': fs})
    bt.when_pressed(play)
    pause()

if __name__=='__main__':
    main()