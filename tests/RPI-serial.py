import serial
from time import sleep

srl = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
print(f"Writable: {srl.writable()}")
sleep(2)
with srl as s:
    s.write(b'REQ')
    while True:
        x = s.read(2)
        print(f"Se recibió: {x}")
        if x != b"OK": continue
        print("¡La prueba terminó de forma exitosa!")
        break
