from MotorController import MotorController
import threading
from flask_socketio import SocketIO
import time
from kinematics_utils import forward_kinematics, degrees_to_radians

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
            'theta3': self.motor3_controller.get_current_angle(),
        }
        return log
    
    def thread_function(self):
        socketio_instance = self.socketio_instance
        while True:
            angles_as_string = self.get_angles()
            end_effector_position = forward_kinematics(
                degrees_to_radians(angles_as_string['theta1']),
                degrees_to_radians(90),  # Assuming 'theta2' is zero as per your current code.
                degrees_to_radians(angles_as_string['theta3']),
                1, 1, 1
            )

            # Combine the angles and position data into one dictionary
            final_data = {
                'theta1': angles_as_string['theta1'],
                'theta2': 90,  # 'theta2' is hard-coded as zero in this context.
                'theta3': angles_as_string['theta3'],
                'x': end_effector_position['x'],
                'y': end_effector_position['y'],
                'z': end_effector_position['z']
            }

            socketio_instance.emit('angles_data', final_data)
            time.sleep(0.1)

    
    def start_thread(self,):
        this_thread = threading.Thread(target=self.thread_function)
        this_thread.start()
        print('motor monitoring thread started')