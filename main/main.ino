void setup() {
  Serial.begin(9600);
}

void loop() {
  int mq135_analog_value = analogRead(A0);
  int mq3_analog_value = analogRead(A1);
  Serial.print(mq135_analog_value);
  Serial.print(",");
  Serial.println(mq3_analog_value);
  delay(3000);
}
