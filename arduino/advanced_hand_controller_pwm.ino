#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Initialize the Adafruit PWM Servo Driver
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
 
// PWM channels for each servo
// 0 Thumb
// 1 Index finger
// 2 Middle finger
// 3 Ring finger
// 4 Little finger

void setup() {
    Serial.begin(9600);

    // Initialize the PWM driver
    pwm.begin();
    pwm.setPWMFreq(47);  // Set frequency to 50 Hz (standard for servos), customizable

    // Set initial servo positions
    set_servos(0, 0, 0, 0, 0);
}

char receive_buffer[20] = {0};
uint8_t buffer_index = 0;
uint8_t receive_done = 0;

void loop() {
  //Serial.availible does not register more than 1 character on the serial interface because the baute rate is to slow.
	//It works with higher baute rates but those baute rates are instable with an arduino uno.
	//To solve the issue that the uC is to fast without being blocking in the code I added an receive_done bit to know that the end of the message is received.
	//This character must be a character with an ascii value lower than 32 like an enter or a carage return character.
    while (Serial.available()) {
        char received_character = Serial.read();
        if (received_character > 31) {
            receive_buffer[buffer_index] = received_character;
            buffer_index++;
        } else {
            receive_done = 1;
        }
    }

    if (buffer_index == 5 && receive_done) {
        //for (uint8_t i = 0; i < 5; i++) { Serial.println(receive_buffer[i]); }	// for debugging only

        uint8_t legal_input = 1; //checks if the 5 character input is a legal input for the convertion.
        for (uint8_t i = 0; i < 5; i++) {
            if (receive_buffer[i] < '0' || receive_buffer[i] > '9') {
                legal_input = 0;
            }
        }

        if (legal_input) {
            set_servos(
                20 * (receive_buffer[0] - '0'),
                20 * (receive_buffer[1] - '0'),
                20 * (receive_buffer[2] - '0'),
                20 * (receive_buffer[3] - '0'),
                20 * (receive_buffer[4] - '0')
            );
        }
    } else if (receive_done) {
        uint8_t i = 0;
        while (receive_buffer[i] != 0) {
            Serial.print(receive_buffer[i]);
            i++;
        }
        Serial.println();
    }

    if (receive_done) {
        for (uint8_t i = 0; i < sizeof(receive_buffer); i++) {
            receive_buffer[i] = 0;
        }
        buffer_index = 0;
        receive_done = 0;
    }
}

// Function to set servos to the given angles
void set_servos(uint8_t angle_s0, uint8_t angle_s1, uint8_t angle_s2, uint8_t angle_s3, uint8_t angle_s4) {
    const uint16_t MIN_PULSE = 50;  // Minimum pulse length, neeed to be calibrated according to the servos
    const uint16_t MAX_PULSE = 200;  // Maximum pulse length, neeed to be calibrated according to the servos
    
    uint16_t servo_pulses[] = {
        map(180 - angle_s0, 0, 180, MIN_PULSE, MAX_PULSE),  // Thumb (reversed)
        map(angle_s1, 0, 180, MIN_PULSE, MAX_PULSE),       // Index
        map(angle_s2, 0, 180, MIN_PULSE, MAX_PULSE),       // Middle
        map(angle_s3, 0, 180, MIN_PULSE, MAX_PULSE),       // Ring
        map(angle_s4, 0, 180, MIN_PULSE, MAX_PULSE)        // Little
    };

    for (uint8_t i = 0; i < 5; i++) {
        pwm.setPWM(i, 4095-servo_pulses[i], servo_pulses[i]);
    }
}
