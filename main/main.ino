void setup() {
  Serial.begin(9600);
}

void loop() {
  int mq135_analog_value = analogRead(A0);
  int mq3_analog_value = analogRead(A1);

  float voltage_mq135 = mq135_analog_value * (5.0 / 1023.0);
  float voltage_mq3 = mq3_analog_value * (5.0 / 1023.0); 

  Serial.print(voltage_mq135);
  Serial.print(",");
  Serial.println(voltage_mq3);
  delay(1000);
}
