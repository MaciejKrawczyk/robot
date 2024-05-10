import RPi.GPIO as GPIO

class ReadingPin:
    def __init__(self, pin_number: int) -> None:
        self.pin_number = pin_number
        GPIO.setup(self.pin_number, GPIO.IN)