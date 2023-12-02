import json
from gtts import gTTS
from io import BytesIO
from shutil import rmtree
from os import mkdir
from pydub import AudioSegment

def main():
    F = open("textos.json", "r")
    data = json.load(F)
    F.close()
    try: rmtree('audio')
    except: pass
    finally: mkdir('audio')
    for i in range(len(data)):
        if (len(data[i]) <= 100):
            obj = gTTS(data[i], lang='es')
            F = open(f"audio/{i}.wav", 'wb+')
            audio=AudioSegment.from_mp3(BytesIO(list(obj.stream())[0]))
            audio.export(f"audio/{i}.wav", format='wav')
            F.close()
        else:
            c=0
            limit=100
            L=[]
            t=''
            objL = None
            w=data[i].split()
            for e in w:
                if len(t+e+' ') > 100:
                    L.append(t)
                    t = ''
                t += e+' '
            if t: 
                L.append(t)
                t=''
            for e in L:
                obj=BytesIO(list(gTTS(e, lang='es').stream())[0])
                if not objL:
                    objL = AudioSegment.from_file(obj)
                else:
                    objL += AudioSegment.from_file(obj)
            objL.export(f"audio/{i}.wav", format='wav')

if __name__=='__main__':
    main()
