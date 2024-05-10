import time
import RPi.GPIO as GPIO
import numpy as np
import math
from .PWMChannel import PWMChannelForMotor

PULSES_PER_REVOLUTION = 1220


def wrap_angle(angle):
    return (angle + np.pi) % (2 * np.pi)


def degrees_to_radians(degrees: float):
    radians = degrees * (math.pi / 180)
    return radians


class MotorEncoderCombo_i2c:
    def __init__(
        self, 
        reading_plus_pin,
        reading_minus_pin,
        pwm_channel_plus: PWMChannelForMotor,
        pwm_channel_minus: PWMChannelForMotor, 
        starting_angle = 0,
        is_minus_plus_swapped = False,
        pulses_per_revolution=PULSES_PER_REVOLUTION
        ):
        self.pwm_channel_plus = pwm_channel_plus
        self.pwm_channel_minus = pwm_channel_minus
        self.reading_plus_pin = reading_plus_pin
        self.reading_minus_pin = reading_minus_pin
        self.pulses_per_revolution = pulses_per_revolution
        self._pulses = 0
        self.is_minus_plus_swapped = is_minus_plus_swapped
        self.starting_angle = starting_angle
        
        # GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.reading_plus_pin, GPIO.IN)
        GPIO.setup(self.reading_minus_pin, GPIO.IN)

        GPIO.add_event_detect(self.reading_plus_pin, GPIO.RISING, callback=self._read_encoder)


    def _read_encoder(self, channel):
        b = GPIO.input(self.reading_minus_pin)
        self._pulses += 1 if b > 0 else -1

        
    def get_pulses(self):
        return self._pulses


    def get_angle(self):
        angle = ((self._pulses * 360) / self.pulses_per_revolution) + self.starting_angle
        return angle


    def run_motor(self, direction, percent_of_power):
        if not self.is_minus_plus_swapped:
            if direction == "plus":
                self.pwm_channel_minus.stop()
                self.pwm_channel_plus.run_at(percent_of_power)
            elif direction == "minus":
                self.pwm_channel_minus.run_at(percent_of_power)
                self.pwm_channel_plus.stop()
            else:
                raise Exception("Invalid direction")
        else:
            if direction == "minus":
                self.pwm_channel_minus.stop()
                self.pwm_channel_plus.run_at(percent_of_power)
            elif direction == "plus":
                self.pwm_channel_minus.run_at(percent_of_power)
                self.pwm_channel_plus.stop()
            else:
                raise Exception("Invalid direction")
                
                
    def stop(self):
        self.pwm_channel_minus.stop()
        self.pwm_channel_plus.stop()
        
