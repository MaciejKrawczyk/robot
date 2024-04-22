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
            # motor2_controller: MotorController,
            motor3_controller: MotorController
    ) -> None:
        self.motor1_controller = motor1_controller
        # self.motor2_controller = motor2_controller
        self.motor3_controller = motor3_controller
        self.socketio_instance = socketio_instance
        
    def get_angles(self):
        log = {
            'theta1': self.motor1_controller.get_current_angle(),
            # 'theta2': self.motor2_controller.get_current_angle(),
            'theta2': 90,
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
            # angles_as_string = self.get_angles()
            # end_effector_position = forward_kinematics(
            #     degrees_to_radians(angles_as_string['theta1']),
            #     degrees_to_radians(90),  # Assuming 'theta2' is zero as per your current code.
            #     degrees_to_radians(angles_as_string['theta3']),
            #     1, 1, 1
            # )
            

            # Combine the angles and position data into one dictionary
            # final_data = {
            #     'theta1': angles_as_string['theta1'],
            #     'theta2': 90,  # 'theta2' is hard-coded as zero in this context.
            #     'theta3': angles_as_string['theta3'],
            #     'x': end_effector_position['x'],
            #     'y': end_effector_position['y'],
            #     'z': end_effector_position['z']
            # }
            angles = self.get_angles()
            pos = self.get_position(angles)
            final_data = self.get_position_and_angles(pos, angles)

            socketio_instance.emit('angles_data', final_data)
            time.sleep(0.1)

    
    def start_thread(self,):
        this_thread = threading.Thread(target=self.thread_function)
        this_thread.start()
        print('motor monitoring thread started')