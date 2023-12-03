#include <Servo.h>

int servo1 = 6;
Servo oreja1;
int servo2 = 5;
Servo oreja2;
int servo3 = 3;
Servo cola;

int orejasF1 = 90;
int colaF1 = 130;
int colaF2 = 60;

int orejasT1 = 180;
int colaT1 = 50;
int colaT2 = 70;

int orejasI1 = 180;
int colaI1 = 120;

int orejasM1 = 30;
int colaM1 = 10;

int orejasA1 = 90;
int orejasA2 = 20;
int colaA1 = 10;

int orejasN1 = 90;
int colaN1 = 90;

void dialogo1(){
  oreja1.write(orejasF1);
  oreja2.write(orejasF1);
  
  cola.write(colaF1);
  delay(800);
  cola.write(colaF2);
  delay(800);
  }

void dialogo2(){
  oreja1.write(orejasT1);
  oreja2.write(orejasT1);
  
  cola.write(colaF1);
  delay(800);
  cola.write(colaF2);
  delay(800);
}

void dialogo3(){
   oreja1.write(orejasF1);
   oreja2.write(orejasF1);
  
  cola.write(colaF1);
}

void dialogo4(){
  oreja1.write(orejasF1);
  oreja2.write(orejasF1);
  
  cola.write(colaF1);
  delay(800);
  cola.write(colaF2);
  delay(800);
}
void dialogo5(){
 oreja1.write(orejasF1);
  oreja2.write(orejasF1);
  
  cola.write(colaF1);
}
void dialogo6(){
  oreja1.write(orejasI1);
  oreja2.write(orejasI1);
  
  cola.write(colaI1);
}

String seRead() {
  String a;
  while (1) {
    if (Serial.available() > 0) {
      char r = Serial.read();
      if (r == '\n') return a;
      a += r;
    }}
}

typedef void (*Dialogo)(void);
int diagc = 0;
Dialogo funcs[] = {dialogo1, dialogo2, dialogo3,
                  dialogo4, dialogo5, dialogo6};

void setup() {
  oreja1.attach(servo1);
  Serial.begin(9600);
  oreja2.attach(servo2);
  Serial.begin(9600);
  cola.attach(servo3);
  Serial.begin(9600);
}

void loop() {
  String s = seRead();
  if (s == "next") {
    funcs[diagc]();
    diagc++;
  }
}
