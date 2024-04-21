import threading

import RPi.GPIO as GPIO
import time

from MotorEncoderCombo import MotorEncoderCombo
from MotorController import MotorController



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


def task_move_theta1_to(theta1_controller: MotorController, degree: float):
    theta1_controller.move_to(degree, hold=True)

def task_move_theta2_to(theta2_controller: MotorController, degree: float):
    theta2_controller.move_to(degree, hold=True)

def task_move_theta3_to(theta3_controller: MotorController, degree: float):
    theta3_controller.move_to(degree, hold=True)

def task_move_theta1(theta1_controller: MotorController, direction: str):
    theta1_controller.run(direction=direction)

def task_move_theta2(theta2_controller: MotorController, direction: str):
    theta2_controller.run(direction=direction)

def task_move_theta3(theta3_controller: MotorController, direction: str):
    theta3_controller.run(direction=direction)


def all3Motors(
        calculated_theta1,
        calculated_theta2,
        calculated_theta3,
        motor_theta1_controller,
        # motor_theta2_controller,
        motor_theta3_controller,
        current_theta1,
        # current_theta2,
        current_theta3
    ):
    threads = []
    if current_theta1 != calculated_theta1:
        thread1 = threading.Thread(target=task_move_theta1_to, args=(motor_theta1_controller, calculated_theta1))
        thread1.start()
        threads.append(thread1)

    # if current_theta2 != calculated_theta2:
    #   thread2 = threading.Thread(target=task_move_theta2_to, args=(motor_theta2_controller, calculated_theta2))
    #   thread2.start()
    #   threads.append(thread2)

    if current_theta3 != calculated_theta3:
        thread3 = threading.Thread(target=task_move_theta3_to, args=(motor_theta3_controller, calculated_theta3))
        thread3.start()
        threads.append(thread3)
    
    for thread in threads:
        print(thread)
        thread.join()    

def All3MotorsTaskStart(
        theta1: float,
        theta2: float,
        theta3: float,
        motor_theta1_controller: MotorController,
        # motor_theta2_controller: MotorController,
        motor_theta3_controller: MotorController,
        current_theta1,
        # current_theta2,
        current_theta3
    ):
    calculated_theta1 = theta1
    calculated_theta2 = theta2
    calculated_theta3 = theta3
    threading.Thread(target=all3Motors, args=(
        calculated_theta1, 
        calculated_theta2, 
        calculated_theta3,
        motor_theta1_controller,
        # motor_theta2_controller,
        motor_theta3_controller,
        current_theta1,
        # current_theta2,
        current_theta3
        )
    ).start()

def motor1MovePlusTaskStart():
    threading.Thread(
        target=task_move_theta1, args=('plus') 
    ).start()

def motor1MoveMinusTaskStart():
    threading.Thread(
        target=task_move_theta1, args=('minus') 
    ).start()

class RRRRobot:
    def __init__(self) -> None:
        motors_controllers = init_robot()
        self.motor_theta1_controller = motors_controllers['motor_theta1_controller']
        
        # self.motor_theta2_controller = motors_controllers['motor_theta2_controller']

        self.motor_theta3_controller = motors_controllers['motor_theta3_controller']
        
        

    def move_to(self, x: float, y: float, z: float):
        # calculate the degress of each motor using kinematics...
        calculated_theta1 = 90
        calculated_theta2 = 90
        calculated_theta3 = 90
        All3MotorsTaskStart(
            calculated_theta1, 
            calculated_theta2, 
            calculated_theta3,
            self.motor_theta1_controller,
            # self.motor_theta2_controller,
            self.motor_theta3_controller,
            current_theta1=self.get_current_theta1(),
            # current_theta2=self.get_current_theta2(),
            current_theta3=self.get_current_theta3()
        )
        
    def move_motor1(self, direction):
        # self.motor_theta1_controller.run(direction=direction)
        if direction == 'plus':
            task_move_theta1(self.motor_theta1_controller, direction=direction)
        else:
            task_move_theta1(self.motor_theta1_controller, direction=direction)

    # def move_motor2(self):
    #     self.motor_theta2_controller.run()

    def move_motor3(self, direction):
        self.motor_theta3_controller.run(direction=direction)

    def stop_motor1(self):
        self.motor_theta1_controller.stop()

    # def stop_motor2(self):
    #     self.motor_theta2_controller.stop()

    def stop_motor3(self):
        self.motor_theta3_controller.stop()


    def move_motor1_by(self, degree: float):
        pass

    def move_motor2_by(self, degree: float):
        pass

    def move_motor3_by(self, degree: float):
        pass

    def move_by(self, theta1: float, theta2: float, theta3: float):
        All3MotorsTaskStart(
            theta1=theta1, 
            theta2=theta2, 
            theta3=theta3, 
            motor_theta1_controller=self.motor_theta1_controller,
            # motor_theta2_controller=self.motor_theta2_controller, 
            motor_theta3_controller=self.motor_theta3_controller,
            current_theta1=self.get_current_theta1(),
            # current_theta2=self.get_current_theta2(),
            current_theta3=self.get_current_theta3()
        )
    
    def get_current_theta1(self,):
        return self.motor_theta1_controller.motor.get_angle()


    def get_current_theta2(self, ):
        return self.motor_theta2_controller.motor.get_angle()


    def get_current_theta3(self, ):
        return self.motor_theta3_controller.motor.get_angle()
    