from flask import Flask, jsonify, request
import threading
import time
from RRRRobotAPI import RRRRobot
from flask_socketio import SocketIO
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fh09g3f2qo8hrf093bf783brc9y71gb37fhr31chobr1uvb2bv'
socketio = SocketIO(app, cors_allowed_origins="*")
robotAPI = RRRRobot()
CORS(app)

def emit_current_angle():
    while True:
        current_angle = robotAPI.motor_theta1_controller.motor.get_angle()
        print(current_angle)
        socketio.emit('command_response', {'angle': current_angle})
        time.sleep(0.1)  # Adjust sleep time as necessary

# Modify this function to start a second process for emitting the angle constantly
def start_background_tasks():
    # Starting the thread for emitting current angle of motor1
    angle_thread = Thread(target=emit_current_angle)
    angle_thread.daemon = True  # Daemon threads are shut down immediately when the program exits
    angle_thread.start()

@socketio.on('send-command')
def handle_command(command_object):

    available_commands = ['theta1+', 'theta1-', 'theta2+', 'theta2-', 'theta2+', 'theta2-', 'move-to', 'move-by', 'sleep', 'stop_theta1', 'stop_theta2', 'stop_theta3']

    command_name = command_object['name']
    command_body = command_object['body']

    if command_name not in available_commands:
        return jsonify({"error": "command is not available!"})




    match command_name:
        case 'stop_theta1':
            robotAPI.stop_motor1()
        case 'theta1+':
            robotAPI.move_motor1('plus')
        case 'theta1-':
            robotAPI.move_motor1('minus')
        # case _:


    if command_name == 'stop_theta2':
        pass

    if command_name == 'stop_theta3':
        robotAPI.stop_motor3()

    if command_name == 'theta2+':
        pass

    if command_name == 'theta2-':
        pass

    if command_name == 'theta3+':
        pass

    if command_name == 'theta3-':
        pass

    if command_name == 'sleep':
        pass

    if command_name == 'move-by':
        pass

    if command_name == 'move-to':
        pass

    print(f'received command: {command_object}')


@app.route('/move-to', methods=['POST'])
def move_to():

    if not request.is_json:
        return jsonify({"error": "Request must be json"})

    body = request.get_json()
    x = float(body.get('x'))
    y = float(body.get('y'))
    z = float(body.get('z'))

    if x is None or y is None or z is None:
        return jsonify({"error": "x, y or z is not defined"})


    robotAPI.move_to(x, y, z)

    return jsonify({'message': 'Threads triggered'})


@app.route('/move-by', methods=['POST'])
def move_by():

    if not request.is_json:
        return jsonify({"error": "Request must be json"})

    body = request.get_json()
    theta1 = float(body.get('theta1'))
    theta2 = float(body.get('theta2'))
    theta3 = float(body.get('theta3'))

    if theta1 is None or theta2 is None or theta3 is None:
        return jsonify({"error": "theta1, theta2 or theta3 is not defined"})

    robotAPI.move_by(theta1=theta1, theta2=theta2, theta3=theta3)

    return jsonify({'message': 'task in progress'})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    start_background_tasks()
