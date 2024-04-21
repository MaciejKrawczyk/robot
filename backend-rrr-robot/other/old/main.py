
import RPi.GPIO as GPIO
import time

from MotorEncoderCombo import MotorEncoderCombo
from MotorController import MotorController
    

    
GPIO.setmode(GPIO.BCM)

MOTOR_THETA1_PLUS_INPUT_PIN = 27
MOTOR_THETA1_MINUS_INPUT_PIN = 17

MOTOR_THETA1_PLUS_OUTPUT_PIN = 23
MOTOR_THETA1_MINUS_OUTPUT_PIN = 24

MOTOR_THETA2_PLUS_INPUT_PIN = 9
MOTOR_THETA2_MINUS_INPUT_PIN = 10

MOTOR_THETA2_PLUS_OUTPUT_PIN = 8
MOTOR_THETA2_MINUS_OUTPUT_PIN = 7

MOTOR_THETA3_PLUS_INPUT_PIN = 3
MOTOR_THETA3_MINUS_INPUT_PIN = 2

MOTOR_THETA3_PLUS_OUTPUT_PIN = 14
MOTOR_THETA3_MINUS_OUTPUT_PIN = 15

# ------------

motor_theta1 = MotorEncoderCombo(MOTOR_THETA1_PLUS_INPUT_PIN, MOTOR_THETA1_MINUS_INPUT_PIN, MOTOR_THETA1_PLUS_OUTPUT_PIN, MOTOR_THETA1_MINUS_OUTPUT_PIN)
motor_theta1_controller = MotorController(motor_theta1)

motor_theta2 = MotorEncoderCombo(MOTOR_THETA2_PLUS_INPUT_PIN, MOTOR_THETA2_MINUS_INPUT_PIN, MOTOR_THETA2_PLUS_OUTPUT_PIN, MOTOR_THETA2_MINUS_OUTPUT_PIN)
motor_theta2_controller = MotorController(motor_theta2)

#motor_theta3 = MotorEncoderCombo(MOTOR_THETA3_PLUS_INPUT_PIN, MOTOR_THETA3_MINUS_INPUT_PIN, MOTOR_THETA1_PLUS_OUTPUT_PIN, MOTOR_THETA3_MINUS_OUTPUT_PIN)
#motor_theta3_controller = MotorController(motor_theta3)

try: 
    while True:
       print(motor_theta2.get_angle())
        # motor_theta1_controller.move_to(180)
        # time.sleep(1)
        # motor_theta1_controller.move_to(0)
        # time.sleep(1)
        # motor_theta2_controller.move_to(360)
        # time.sleep(1)
        # motor_theta2_controller.move_to(0)
        # time.sleep(1)
    #motor_theta3_controller.move_to(30)
    #time.sleep(1)
    #motor_theta3_controller.move_to(0)
    # motor_theta1_controller.move_to(90)
    # motor_theta1_controller.move_to(180)
    

except KeyboardInterrupt:
    print("Shutting down gracefully...")
    GPIO.cleanup()
    quit()
    
except Exception as e:
    print("An error occurred:", e)
    GPIO.cleanup()
    quit()
