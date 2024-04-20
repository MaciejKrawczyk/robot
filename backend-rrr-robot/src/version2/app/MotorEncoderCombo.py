import time
import RPi.GPIO as GPIO

PULSES_PER_REVOLUTION = 1220

class MotorEncoderCombo:
    def __init__(
        self, 
        input_plus_pin,
        input_minus_pin, 
        output_plus_pin,
        output_minus_pin,
        starting_angle = 0,
        pulses_per_revolution=PULSES_PER_REVOLUTION
        ):
        self.output_plus_pin = output_plus_pin
        self.output_minus_pin = output_minus_pin
        self.input_plus_pin = input_plus_pin
        self.input_minus_pin = input_minus_pin
        self.pulses_per_revolution = pulses_per_revolution
        self._pulses = 0
        
        # GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.input_plus_pin, GPIO.IN)
        GPIO.setup(self.input_minus_pin, GPIO.IN)

        GPIO.setup(self.output_plus_pin, GPIO.OUT)
        GPIO.setup(self.output_minus_pin, GPIO.OUT)

        self.pwm_output_plus = GPIO.PWM(self.output_plus_pin, 1000)
        self.pwm_output_minus = GPIO.PWM(self.output_minus_pin, 1000)

        GPIO.add_event_detect(self.input_plus_pin, GPIO.RISING, callback=self._read_encoder)

    def _read_encoder(self, channel):
        b = GPIO.input(self.input_minus_pin)
        self._pulses += 1 if b > 0 else -1
        
    def get_pulses(self):
        return self._pulses

    def get_angle(self):
        return (self._pulses * 360) / self.pulses_per_revolution

    def set_angle(self, angle):
        # This method can be expanded to include logic for moving the motor to the desired angle
        pass

    def run_motor(self, direction, percent_of_power):
        if direction == "plus":
            # print("run_motor: plus")
            self.pwm_output_minus.start(0)
            self.pwm_output_plus.start(percent_of_power)
        elif direction == "minus":
            # print("run_motor: minus")
            self.pwm_output_plus.start(0)
            self.pwm_output_minus.start(percent_of_power)
        else:
            print("run_motor: invalid direction")
            raise Exception("Invalid direction")
                
    def stop(self):
        """Stop the motor by setting both PWM outputs to 0% duty cycle."""
        self.pwm_output_plus.ChangeDutyCycle(0)
        self.pwm_output_minus.ChangeDutyCycle(0)
        
    def measure_speed(self, measure_time=1):

        initial_time = time.time()
        initial_pulses = self.get_pulses()

        # Wait for the specified measurement time
        time.sleep(measure_time)

        final_time = time.time()
        final_pulses = self.get_pulses()

        # Calculate the number of pulses during the measurement interval
        pulses_count = final_pulses - initial_pulses

        # Calculate the time elapsed in seconds
        time_elapsed = final_time - initial_time

        # Calculate the number of revolutions (one revolution = pulses_per_revolution)
        revolutions = pulses_count / self.pulses_per_revolution

        # Convert the time to minutes and calculate RPM
        time_in_minutes = time_elapsed / 60
        rpm = revolutions / time_in_minutes

        return rpm
