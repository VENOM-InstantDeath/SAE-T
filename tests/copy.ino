String seRead() {
  String a;
  while (1) {
    if (Serial.available() > 0) {
      char r = Serial.read();
      if (r == '\n') return a;
      a += r;
    }}
}

while (1) {
	String s = seRead();
	if (s == "Anger") ira();
	if (s == "Fear"); miedo();
	if (s == "Disgust") disgusto();
	if (s == "Neutral") neutral();
	if (s == "Sadness") tristeza();
	if (s == "Happiness") alegria();
}
