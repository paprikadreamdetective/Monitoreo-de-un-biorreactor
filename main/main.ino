#include <UnorderedMap.h>
/*
int i = 0;
int j = 10;
*/

void setup() {
  Serial.begin(9600);
}

void loop() {
  int mq135_analog_value = analogRead(A0);
  int mq3_analog_value = analogRead(A1);
  Serial.print(mq135_analog_value);
  Serial.print(",");
  Serial.println(mq3_analog_value);
  /*if ( i >= 20 && j >= 30) {
    i = 0;
    j = 10;
  }*/
  /*Serial.print(i);
  Serial.print(",");
  Serial.println(j);
  i++;
  j++;*/
  delay(3000);
}
