#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <FastLED.h>

// Initialize the Adafruit PWM Servo Driver
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
 
// PWM channels for each servo
// 0 Thumb
// 1 Index finger
// 2 Middle finger
// 3 Ring finger
// 4 Little finger

#define Magnet_pin 5
#define Magnet_PWM 6

#define pause_button 2

#define LED_DATA_PIN 11
#define NUM_LEDS 420 //60 leds/m	7 meter strip
CRGB leds[NUM_LEDS];

void setup() {
    Serial.begin(9600);

    // Initialize the PWM driver
    pwm.begin();
    pwm.setPWMFreq(47);  // Set frequency to 50 Hz (standard for servos), customizable

    // Set initial servo positions
    set_servos(0, 0, 0, 0, 0);

	// Set IO Magnet
	pinMode(Magnet_pin, OUTPUT);
	pinMode(Magnet_PWM, OUTPUT);
	digitalWrite(Magnet_pin, 0);
	analogWrite(Magnet_PWM, 0);

	// Set IO Pause button
	pinMode(pause_button, INPUT_PULLUP);
	attachInterrupt(digitalPinToInterrupt(pause_button), ISR_pause_button, CHANGE);

	//Set IO LED strip
	FastLED.addLeds<NEOPIXEL, LED_DATA_PIN>(leds, NUM_LEDS);
	for (uint16_t i = 0; i < NUM_LEDS; i++){
		leds[i].setRGB( 0, 0, 0);
	}
}

uint8_t led_update_bit = 0;

volatile uint8_t pause_state = false;

void loop() {
	char last_received = '\0';
	String receive_buffer = "";

	while(last_received != '\n'){
		if (Serial.available()){
			last_received = Serial.read();
			if (last_received != '\n'){
				receive_buffer += last_received;
			}
		}
	}
	//Serial.println(receive_buffer);		//for debugging

	if (receive_buffer != ""){
    	if (receive_buffer.length() == 5) {
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
    	} else if (receive_buffer != "") {
			if(receive_buffer.equals("pause_state")){
				if (pause_state){
					Serial.println("TRUE");
					pause_state = false;
				}
				else {
					Serial.println("FALSE");
				}
			}
			else if(receive_buffer.equals("magnet ON")){
				digitalWrite(Magnet_pin, 1);
				digitalWrite(Magnet_PWM, 1);
			}
			else if(receive_buffer.equals("magnet OFF")){
				digitalWrite(Magnet_pin, 0);
				digitalWrite(Magnet_PWM, 0);
			}
			else {
				//Serial.println(receive_buffer.length());
        		Serial.println(receive_buffer);
			}
    	}
	}

	if (bitRead(millis(), 11) == led_update_bit){
		FastLED.show();
		led_update_bit != led_update_bit;
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

void ISR_pause_button(){
	pause_state = true;
}