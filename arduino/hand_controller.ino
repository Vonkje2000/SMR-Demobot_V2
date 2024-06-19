#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

void setup() {
  Serial.begin(9600);

  servo1.attach(3); //Thumb
  servo2.attach(5); //Index finger
  servo3.attach(6); //Middle finger
  servo4.attach(9); //Ring finger
  servo5.attach(10); //Little finger
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    switch (command) {
      case '0':  // Stone position
        servo1.write(180);
        servo2.write(0);
        servo3.write(0);
        servo4.write(0);
        servo5.write(0);
        break;
      case '1':  // Paper position
        servo1.write(0);
        servo2.write(180);
        servo3.write(180);
        servo4.write(180);
        servo5.write(180);
        break;
      case '2':  // Scissors position
        servo1.write(180);
        servo2.write(180);
        servo3.write(180);
        servo4.write(0);
        servo5.write(0);
        break;
    }
  }
}
