int counter = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {

  if ( counter >= 20 )
    counter = 0;
  Serial.println(counter);
  counter++;
  delay(250);
}
