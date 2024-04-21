from MotorEncoderCombo import MotorEncoderCombo
from MotorController import MotorController
import RPi.GPIO as GPIO
from typing import List, Tuple

def init_robot():
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

    motor_theta3 = MotorEncoderCombo(MOTOR_THETA2_PLUS_INPUT_PIN, MOTOR_THETA2_MINUS_INPUT_PIN, MOTOR_THETA2_PLUS_OUTPUT_PIN, MOTOR_THETA2_MINUS_OUTPUT_PIN)
    motor_theta3_controller = MotorController(motor_theta3)

    # motor_theta2 = MotorEncoderCombo(MOTOR_THETA3_PLUS_INPUT_PIN, MOTOR_THETA3_MINUS_INPUT_PIN, MOTOR_THETA1_PLUS_OUTPUT_PIN, MOTOR_THETA3_MINUS_OUTPUT_PIN)
    # motor_theta2_controller = MotorController(motor_theta2)

    return {
        'motor_theta1_controller': motor_theta1_controller, 
        # 'motor_theta2_controller': motor_theta2_controller,
        'motor_theta3_controller': motor_theta3_controller
    }


class RobotAPI:
    def __init__(self) -> None:
        motors_controllers = init_robot()
        self.motor1_controller = motors_controllers['motor_theta1_controller']
        # self.motor2_controller = motors_controllers['motor_theta2_controller']
        self.motor3_controller = motors_controllers['motor_theta3_controller']
        
    def get_current_theta1(self) -> float:
        self.motor1_controller.get_current_angle()
    
    def get_current_theta2(self) -> float:
        pass
    
    def get_current_theta3(self) -> float:
        self.motor3_controller.get_current_angle()
    
    def move_to(self, x: float, y: float, z: float):
        pass
    
    def move_to_multiple_points(self, points: List[Tuple[float, float, float]], is_bezier=False):
        pass
    
    def move_by(self, theta1: float, theta2: float, theta3: float):
        pass
    
    def move_motor1_plus(self, speed_percent=100):
        self.motor1_controller.run('plus', percent_of_power=speed_percent)
    
    def move_motor1_minus(self, speed_percent=100):
        self.motor1_controller.run('minus', percent_of_power=speed_percent)
    
    def move_motor2_plus(self, speed_percent=100):
        pass
    
    def move_motor2_minus(self, speed_percent=100):
        pass
    
    def move_motor3_plus(self, speed_percent=100):
        self.motor3_controller.run('plus', percent_of_power=speed_percent)
    
    def move_motor3_minus(self, speed_percent=100):
        self.motor3_controller.run('minus', percent_of_power=speed_percent)
    
    def move_motor1_by(self, degree: float):
        pass
    
    def move_motor2_by(self, degree: float):
        pass
    
    def move_motor3_by(self, degree: float):
        pass    
    
    def stop_motor1(self, ):
        self.motor1_controller.stop()
    
    def stop_motor2(self, ):
        pass
    
    def stop_motor3(self, ):
        self.motor3_controller.stop()
        
    def abort_movement(self,):
        self.stop_motor1
        self.stop_motor2
        self.stop_motor3