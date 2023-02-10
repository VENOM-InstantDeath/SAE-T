void setup() {
  Serial.begin(9600);
}

char* seRead(int nbytes) {
  Serial.flush();
  char *a = new char[nbytes];
  int c = 0;
  while (c != nbytes) {
    if (Serial.available() > 0) {
      char r = Serial.read();
      if (r == '\n') continue;
      a[c] = r;
      c++;
    }
  }
  Serial.flush();
  return a;
}

void loop() {
  char *b = seRead(3);
  Serial.print("OK");
}
