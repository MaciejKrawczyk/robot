import board
from adafruit_pca9685 import PCA9685
import time
from utils.helpers import percent_to_value, decimal_to_hex

from MotorEncoderCombo_i2c import MotorEncoderCombo_i2c
from PWMChannel import PWMChannelForMotor
from ReadingPin import ReadingPin
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def test_motor(motor: MotorEncoderCombo_i2c, motor_id: str):
    print(f'motor {motor_id} angle: {motor.get_angle()}')
    
    motor.run_motor('plus', 50.0)
    time.sleep(0.5)
    motor.stop()
    time.sleep(2)

    print(f'motor {motor_id} angle: {motor.get_angle()}')

    motor.run_motor('minus', 50.0)
    time.sleep(0.5)
    motor.stop()
    time.sleep(2)

    print(f'motor {motor_id} angle: {motor.get_angle()}')

    motor.stop()


i2c = board.I2C()
pca = PCA9685(i2c)
pca.frequency = 1000

percent_of_power = 50
power = percent_to_value(percent=percent_of_power)



MOTOR1_READING_PLUS_PIN_NUMBER = ReadingPin(27)
MOTOR1_READING_MINUS_PIN_NUMBER = ReadingPin(17)

MOTOR2_READING_PLUS_PIN_NUMBER = ReadingPin(5)
MOTOR2_READING_MINUS_PIN_NUMBER = ReadingPin(6)

MOTOR3_READING_PLUS_PIN_NUMBER = ReadingPin(9)
MOTOR3_READING_MINUS_PIN_NUMBER = ReadingPin(10)

MOTOR1_PLUS_PWM_CHANNEL = PWMChannelForMotor(pca.channels[0])
MOTOR1_MINUS_PWM_CHANNEL = PWMChannelForMotor(pca.channels[1])

MOTOR2_PLUS_PWM_CHANNEL = PWMChannelForMotor(pca.channels[2])
MOTOR2_MINUS_PWM_CHANNEL = PWMChannelForMotor(pca.channels[3])

MOTOR3_PLUS_PWM_CHANNEL = PWMChannelForMotor(pca.channels[5])
MOTOR3_MINUS_PWM_CHANNEL = PWMChannelForMotor(pca.channels[4])


MOTOR1_PLUS_PWM_CHANNEL.run_at(60)
time.sleep(0.5)
MOTOR1_PLUS_PWM_CHANNEL.stop()
time.sleep(0.2)

MOTOR1_MINUS_PWM_CHANNEL.run_at(60)
time.sleep(0.5)
MOTOR1_MINUS_PWM_CHANNEL.stop()
time.sleep(0.2)

MOTOR2_PLUS_PWM_CHANNEL.run_at(60)
time.sleep(0.5)
MOTOR2_PLUS_PWM_CHANNEL.stop()
time.sleep(0.2)

MOTOR2_MINUS_PWM_CHANNEL.run_at(60)
time.sleep(0.5)
MOTOR2_MINUS_PWM_CHANNEL.stop()
time.sleep(0.2)

MOTOR3_PLUS_PWM_CHANNEL.run_at(60)
time.sleep(0.5)
MOTOR3_PLUS_PWM_CHANNEL.stop()
time.sleep(0.2)

MOTOR3_MINUS_PWM_CHANNEL.run_at(60)
time.sleep(0.5)
MOTOR3_MINUS_PWM_CHANNEL.stop()
time.sleep(0.2)


# motor1 = MotorEncoderCombo_i2c(
#     MOTOR1_READING_PLUS_PIN_NUMBER, 
#     MOTOR1_READING_MINUS_PIN_NUMBER,
#     MOTOR1_PLUS_PWM_CHANNEL,
#     MOTOR1_MINUS_PWM_CHANNEL,
#     )

# w momencie inicjalizacji drugiej klasy MotorEncoderCombo_i2c
# jest najpierw timeout, a potem no i2c device at address 0x40

# motor2 = MotorEncoderCombo_i2c(
#     MOTOR2_READING_PLUS_PIN_NUMBER, 
#     MOTOR2_READING_MINUS_PIN_NUMBER,
#     MOTOR2_PLUS_PWM_CHANNEL,
#     MOTOR2_MINUS_PWM_CHANNEL,
#     )

# motor3 = MotorEncoderCombo_i2c(
#     MOTOR3_READING_PLUS_PIN_NUMBER, 
#     MOTOR3_READING_MINUS_PIN_NUMBER,
#     MOTOR3_PLUS_PWM_CHANNEL,
#     MOTOR3_MINUS_PWM_CHANNEL,
#     )


# test_motor(motor1, '1')
# test_motor(motor2, '2')
# test_motor(motor3, '3')



# TO PONIŻEJ DZIAŁA!!!!

# pca.channels[0].duty_cycle = 0x0   # motor_theta1 counter clockwise
# pca.channels[1].duty_cycle = power

# time.sleep(0.5)

# pca.channels[0].duty_cycle = power  # motor_theta1 clockwise
# pca.channels[1].duty_cycle = 0x0

# time.sleep(0.5)

# pca.channels[0].duty_cycle = 0 
# pca.channels[1].duty_cycle = 0x0

# ######

# pca.channels[2].duty_cycle = power   # motor_theta2 clockwise
# pca.channels[3].duty_cycle = 0x0

# time.sleep(0.5)

# pca.channels[2].duty_cycle = 0x0   # motor_theta2 clockwise
# pca.channels[3].duty_cycle = 0xffff

# time.sleep(0.5)

# pca.channels[2].duty_cycle = 0x0   # motor_theta2 clockwise
# pca.channels[3].duty_cycle = 0


# pca.channels[4].duty_cycle = 0x0   # motor_theta3
# pca.channels[5].duty_cycle = power

# time.sleep(0.5)

# pca.channels[4].duty_cycle = power   # motor_theta3
# pca.channels[5].duty_cycle = 0x0

# time.sleep(0.5)

# pca.channels[4].duty_cycle = 0   # motor_theta3
# pca.channels[5].duty_cycle = 0x0