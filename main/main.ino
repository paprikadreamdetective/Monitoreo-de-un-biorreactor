#include <UnorderedMap.h>

int i = 0;
int j = 10;


void setup() {
  Serial.begin(9600);
}

void loop() {

  if ( i >= 20 && j >= 30) {
    i = 0;
    j = 10;
  }
  Serial.print(i);
  Serial.print(",");
  Serial.println(j);
  i++;
  j++;
  delay(250);
}
