from RRRRobotAPI2 import RobotAPI
import time

robotAPI = RobotAPI()

print(robotAPI.get_current_theta1())
print(robotAPI.get_current_theta2())
print(robotAPI.get_current_theta3())

robotAPI.move_motor1_minus(60)
time.sleep(0.5)
robotAPI.move_motor1_plus(60)
time.sleep(0.5)
robotAPI.move_motor2_minus(60)
time.sleep(0.5)
robotAPI.move_motor2_plus(60)
time.sleep(0.5)
robotAPI.move_motor3_minus(60)
time.sleep(0.5)
robotAPI.move_motor3_plus(60)

print(robotAPI.get_current_theta1())
print(robotAPI.get_current_theta2())
print(robotAPI.get_current_theta3())