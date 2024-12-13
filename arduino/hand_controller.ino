#include <Servo.h>

Servo servos[5];

int servo_pins[] = {3,5,6,9,10};
// 0 Thumb
// 1 Index finger
// 2 Middle finger
// 3 Ring finger
// 4 Little finger

void setup() {
	Serial.begin(9600);

	int servo_angles[] = {180, 0, 0, 0, 0};
	for (int i = 0; i < sizeof(servos); i++){
		servos[i].attach(servo_pins[i]);
		servos[i].write(servo_angles[i]);
	}
}

char command = '0';

void loop() {
	
	if (Serial.available() > 0) {
		command = Serial.read();
	}

    switch (command) {
	case '0':  // Stone position
	  	set_servos(0, 0, 0, 0, 0);
        break;
	case '1':  // Paper position
	  	set_servos(180, 180, 180, 180, 180);
        break;
	case '2':  // Scissors position
	  	set_servos(0, 180, 180, 0, 0);
        break;
	case '3':  // thunb up
        set_servos(180, 0, 0, 0, 0);
        break;
	case '4':  // middle finger
        set_servos(180, 0, 180, 0, 0);
        break;
	case '5':  // middle finger
        set_servos(180, 180, 0, 0, 180);
        break;
	case '6':  // middle finger
		set_servos(180, 180, 0, 0, 180);
		for (int i = 0; i < 10; i++){
			set_servos(180, 180, 45, 45, 180);
			delay(100);
			set_servos(180, 180, 135, 135, 180);
			delay(100);
		}
		break;
	case '7':  // pistol finger
        set_servos(180, 180, 0, 0, 0);
        break;
	case '8':  // oke finger
        set_servos(0, 0, 180, 180, 180);
        break;
	case '+':  // count up finger
		set_servos(0, 0, 0, 0, 0);
		delay(100);
		set_servos(180, 0, 0, 0, 0);
		delay(100);
		set_servos(180, 180, 0, 0, 0);
		delay(100);
		set_servos(180, 180, 180, 0, 0);
		delay(100);
		set_servos(180, 180, 180, 180, 0);
		delay(100);
		set_servos(180, 180, 180, 180, 180);
		break;
	case '-':  // count up finger
		set_servos(180, 180, 180, 180, 180);
		delay(100);
		set_servos(180, 180, 180, 180, 0);
		delay(100);
		set_servos(180, 180, 180, 0, 0);
		delay(100);
		set_servos(180, 180, 0, 0, 0);
		delay(100);
		set_servos(180, 0, 0, 0, 0);
		delay(100);
		set_servos(0, 0, 0, 0, 0);
		break;
  }
  delay(100);
}

void set_servos(int angle_s0, int angle_s1, int angle_s2, int angle_s3, int angle_s4){
int servo_angles[] = {180 - angle_s0, angle_s1, angle_s2, angle_s3, angle_s4};
	for (int i = 0; i < sizeof(servos); i++){
		servos[i].write(servo_angles[i]);
	}
}
