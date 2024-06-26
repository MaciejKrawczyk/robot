from .MotorEncoderCombo_i2c import MotorEncoderCombo_i2c
from .MotorController import MotorController
from .PWMChannel import PWMChannelForMotor
import RPi.GPIO as GPIO
import board
from adafruit_pca9685 import PCA9685
from config import config


def init_robot():
    i2c = board.I2C()
    pca = PCA9685(i2c)
    pca.reset()
    pca.frequency = 1000

    GPIO.setmode(GPIO.BCM)

    motor1_channel_plus = pca.channels[0]
    motor1_channel_minus = pca.channels[1]
    motor2_channel_plus = pca.channels[2]
    motor2_channel_minus = pca.channels[3]
    motor3_channel_plus = pca.channels[4]
    motor3_channel_minus = pca.channels[5]
    
    MOTOR1_PWM_PLUS = PWMChannelForMotor(motor1_channel_plus)
    MOTOR1_PWM_MINUS = PWMChannelForMotor(motor1_channel_minus)
    
    MOTOR2_PWM_PLUS = PWMChannelForMotor(motor2_channel_plus)
    MOTOR2_PWM_MINUS = PWMChannelForMotor(motor2_channel_minus)
    
    MOTOR3_PWM_PLUS = PWMChannelForMotor(motor3_channel_plus)
    MOTOR3_PWM_MINUS = PWMChannelForMotor(motor3_channel_minus)

    MOTOR_THETA1_PLUS_INPUT_PIN = 27
    MOTOR_THETA1_MINUS_INPUT_PIN = 17

    MOTOR_THETA2_PLUS_INPUT_PIN = 5
    MOTOR_THETA2_MINUS_INPUT_PIN = 6

    MOTOR_THETA3_PLUS_INPUT_PIN = 9
    MOTOR_THETA3_MINUS_INPUT_PIN = 10

    # ------------

    motor_theta1 = MotorEncoderCombo_i2c(MOTOR_THETA1_PLUS_INPUT_PIN, MOTOR_THETA1_MINUS_INPUT_PIN, MOTOR1_PWM_PLUS, MOTOR1_PWM_MINUS, starting_angle=config['DEFAULT_THETA1_POSITION'], is_minus_plus_swapped=True)
    motor_theta1_controller = MotorController(motor_theta1, is_holding_enabled=config['ENABLE_HOLDING_THREAD'], id=1)

    motor_theta2 = MotorEncoderCombo_i2c(MOTOR_THETA2_PLUS_INPUT_PIN, MOTOR_THETA2_MINUS_INPUT_PIN, MOTOR2_PWM_PLUS, MOTOR2_PWM_MINUS, starting_angle=config['DEFAULT_THETA2_POSITION'], is_minus_plus_swapped=True)
    motor_theta2_controller = MotorController(motor_theta2, is_holding_enabled=config['ENABLE_HOLDING_THREAD'], id=2)

    motor_theta3 = MotorEncoderCombo_i2c(MOTOR_THETA3_PLUS_INPUT_PIN, MOTOR_THETA3_MINUS_INPUT_PIN, MOTOR3_PWM_PLUS, MOTOR3_PWM_MINUS, starting_angle=config['DEFAULT_THETA3_POSITION'], is_minus_plus_swapped=True)
    motor_theta3_controller = MotorController(motor_theta3, is_holding_enabled=config['ENABLE_HOLDING_THREAD'], id=3)


    return {
        'motor_theta1_controller': motor_theta1_controller, 
        'motor_theta2_controller': motor_theta2_controller,
        'motor_theta3_controller': motor_theta3_controller
    }


class RobotAPI:
    def __init__(self) -> None:
        motors_controllers = init_robot()
        self.motor1_controller = motors_controllers['motor_theta1_controller']
        self.motor2_controller = motors_controllers['motor_theta2_controller']
        self.motor3_controller = motors_controllers['motor_theta3_controller']
    
        
    def get_current_theta1(self) -> float:
        self.motor1_controller.get_current_angle()
    
    def get_current_theta2(self) -> float:
        self.motor2_controller.get_current_angle()
    
    def get_current_theta3(self) -> float:
        self.motor3_controller.get_current_angle()
    
    def move_motor1_plus(self, speed_percent=100):
        self.motor1_controller.run('plus', percent_of_power=speed_percent)
    
    def move_motor1_minus(self, speed_percent=100):
        self.motor1_controller.run('minus', percent_of_power=speed_percent)
    
    def move_motor2_plus(self, speed_percent=100):
        self.motor2_controller.run('plus', percent_of_power=speed_percent)
    
    def move_motor2_minus(self, speed_percent=100):
        self.motor2_controller.run('minus', percent_of_power=speed_percent)
    
    def move_motor3_plus(self, speed_percent=100):
        self.motor3_controller.run('plus', percent_of_power=speed_percent)
    
    def move_motor3_minus(self, speed_percent=100):
        self.motor3_controller.run('minus', percent_of_power=speed_percent) 
    
    def stop_motor1(self, ):
        self.motor1_controller.stop()
    
    def stop_motor2(self, ):
        self.motor2_controller.stop()
    
    def stop_motor3(self, ):
        self.motor3_controller.stop()
        
    def abort_movement(self,):
        self.stop_motor1
        self.stop_motor2
        self.stop_motor3