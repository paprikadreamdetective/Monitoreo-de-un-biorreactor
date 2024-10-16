#include<unordered_map>

int i = 0;
int j = 0;


void setup() {
  Serial.begin(9600);
}

void loop() {

  if ( counter >= 20 )
    counter = 0;
  Serial.println(counter);
  Serial.println();
  counter++;
  delay(250);
}
