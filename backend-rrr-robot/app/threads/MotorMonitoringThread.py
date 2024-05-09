from MotorController import MotorController
import threading
from flask_socketio import SocketIO
import time
from utils.helpers import degrees_to_radians
from utils.kinematics import forward_kinematics


class MotorMonitoringThread:
    def __init__(
            self, 
            socketio_instance: SocketIO,
            motor1_controller: MotorController, 
            motor2_controller: MotorController,
            motor3_controller: MotorController
    ) -> None:
        self.motor1_controller = motor1_controller
        self.motor2_controller = motor2_controller
        self.motor3_controller = motor3_controller
        self.socketio_instance = socketio_instance
        
    def get_angles(self):
        log = {
            'theta1': self.motor1_controller.get_current_angle(),
            'theta2': self.motor2_controller.get_current_angle(),
            # 'theta2': 90,
            'theta3': self.motor3_controller.get_current_angle(),
        }
        return log
    
    def get_position(self, angles):
        pos = forward_kinematics(
            degrees_to_radians(angles['theta1']),
            degrees_to_radians(angles['theta2']),
            degrees_to_radians(angles['theta3']),
        )
        return pos
        
    def get_position_and_angles(self, pos, angles):
        position_and_angles = dict(pos, **angles)
        return position_and_angles
    
    def get_position_and_angles2(self,):
        angles = self.get_angles()
        pos = self.get_position(angles)
        final_data = self.get_position_and_angles(pos, angles)
        return final_data
    
    def thread_function(self):
        socketio_instance = self.socketio_instance
        while True:
            angles = self.get_angles()
            pos = self.get_position(angles)
            final_data = self.get_position_and_angles(pos, angles)

            socketio_instance.emit('angles_data', final_data)
            time.sleep(0.1)

    
    def start_thread(self,):
        this_thread = threading.Thread(target=self.thread_function)
        this_thread.start()
        print('motor monitoring thread started')