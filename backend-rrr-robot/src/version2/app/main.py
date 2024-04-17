from flask import Flask, jsonify, request
import threading
import time
from flask_socketio import SocketIO
from flask_cors import CORS
from RRRRobotAPI2 import RobotAPI
from threads.MotorMonitoringThread import MotorMonitoringThread
from threads.MotorThread import MotorThread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

robotAPI = RobotAPI()

motor1_controller = robotAPI.motor1_controller
# motor2_controller = robotAPI.motor2_controller  # Uncomment if motor2 is used
motor3_controller = robotAPI.motor3_controller

motor1_thread = MotorThread(socketio, motor1_controller, 1)
# motor2_thread = MotorThread(socketio, motor2_controller)  # Uncomment if motor2 is used
motor3_thread = MotorThread(socketio, motor3_controller, 3)
motor_monitoring_thread = MotorMonitoringThread(
    socketio,
    motor1_controller=motor1_controller, 
    # motor2_controller=motor2_controller,  # Uncomment if motor2 is used
    motor3_controller=motor3_controller
)


##
## socket
##

@socketio.on('send-command')
def handle_command(command_object):
    
    available_commands = ['theta1+', 'theta1-', 'theta2+', 'theta2-', 'theta3+', 'theta3-', 'move-to', 'move-by', 'sleep', 'stop_theta1', 'stop_theta2', 'stop_theta3']

    command_name = command_object['name']
    command_body = command_object['body']

    if command_name not in available_commands:
        return jsonify({"error": "command is not available!"})

    match command_name:
        case 'stop_theta1':
            robotAPI.stop_motor1()
        case 'stop_theta3':
            robotAPI.stop_motor3()
        case 'theta1+':
            robotAPI.move_motor1_plus()
        case 'theta1-':
            robotAPI.move_motor1_minus()
        case 'theta3+':
            robotAPI.move_motor3_plus()
        case 'theta3-':
            robotAPI.move_motor3_minus()
        # case _:
        
    print(f'received command: {command_object}')



##
## rest
##

@app.route('/exec-program', methods=['POST'])
def exec_program():
    
    if not request.is_json:
        return jsonify({"error": "Request must be json"})

    commands = request.get_json()
    
    for command in commands:
        
        name = command['name']
        body = command['body']
        
        match name:
            case 'sleep':
                if (body['seconds'] != None):
                    time.sleep(body['seconds'])
                    pass

            case 'move':
                if (body['x'] is not None and body['y'] is not None and body['z'] is not None):
                    time.sleep(2) # placeholder
                    pass            
    


def start_all_threads():
    motor1_thread.start_thread()
    # motor2_thread.start_thread()  # Uncomment if motor2 is used
    motor3_thread.start_thread()
    motor_monitoring_thread.start_thread()
    print('started all threads...')

if __name__ == '__main__':
    start_all_threads()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
