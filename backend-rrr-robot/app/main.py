from flask import Flask, jsonify, request
import time
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
# from RRRRobotAPI2 import RobotAPI
from RRRRobotAPI2 import RobotAPI
from threads.MotorMonitoringThread import MotorMonitoringThread
from threads.MotorThread import MotorThread
from flask_sqlalchemy import SQLAlchemy
import json
import numpy as np
from routes.routes import api
from services import position, robot_code
from utils.helpers import calculate_velocity, get_filename_datetime
from utils.plot_generation import plot_angles, plot_positions, plot_velocity_with_calculated_velocitites, plot_angle_velocity, plot_position_velocity, plot_all_motor_data
from utils.bezier_trajectory import bezier, add_points
from app import create_app
from models import position


app, socketio = create_app()

robotAPI = RobotAPI()
app.register_blueprint(api)

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


def transform_to_numpy(points):
    # Extract x, y, z coordinates into separate lists
    print(points)
    x_coords = [point['x'] for point in points]
    y_coords = [point['y'] for point in points]
    z_coords = [point['z'] for point in points]
    
    # Stack these lists vertically into a NumPy array
    numpy_array = np.array([x_coords, y_coords, z_coords])
    
    return numpy_array


def calculate_run(movements):
    
    cnt = 1
    step = 0.01
    
    run = {}
    for movement_id, movement in enumerate(movements):
        
        if not isinstance(movement, dict):
            
            print(movement)
            
            run[movement_id] = {'velocities': {'vtheta1': [], 'vtheta2': [], 'vtheta3': []}, 'angles': {'theta1': [], 'theta2': [], 'theta3': []}}
            
            numpy_notation_movement_list = transform_to_numpy(movement)
            # print(f'calculating points, cnt = {cnt}')
            X, Y, Z = add_points(numpy_notation_movement_list, cnt)
            print(f'add_points, X: {X}, Y:{Y}, Z:{Z}')
            # print(f'calculating trajectory, step = {step}s')
            # x_b, y_b, z_b = bezier(X, Y, Z, step)
            
            x, y, z, theta1, theta2, theta3 = bezier(X, Y, Z, step)
            
            # x, y, z, theta1, theta2, theta3 = shortest_path(X, Y, Z, step)
            
            # print(x_b)
            # x, y, z = modify_curve(x_b, y_b, z_b, inverse_kinematics3)
            # print(f'calculating velocities')
            vtheta1, vtheta2, vtheta3 = calculate_velocity(theta1, theta2, theta3, step)
            # print(f'generating graphs')
            total_time = len(x) * step
            plot_angles(
                theta1, theta2, theta3,
                total_time,
                f'{get_filename_datetime()}_movement_{movement_id}_angles_over_time_calculated'
            )
            plot_positions(
                x,y,z,
                total_time,
                f'{get_filename_datetime()}_movement_{movement_id}_position_over_time_calculated'
            )
            plot_angle_velocity(
                vtheta1, vtheta2, vtheta3,
                step, 
                f'{get_filename_datetime()}_movement_{movement_id}_angle_velocity_over_time_calculated'
            )

            run[movement_id]['velocities']['vtheta1'] = vtheta1
            run[movement_id]['velocities']['vtheta2'] = vtheta2
            run[movement_id]['velocities']['vtheta3'] = vtheta3
            run[movement_id]['angles']['theta1'] = theta1
            run[movement_id]['angles']['theta2'] = theta2
            run[movement_id]['angles']['theta3'] = theta3
            
        else:
            run[movement_id] = {'sleep': movement['sleep']}
    
    # print(run)
    return run


@app.route('/api/plot', methods=['POST'])
@cross_origin()
def plot_motor_data():
    plot_all_motor_data()
    return jsonify({'message': 'done'})

@app.route('/api/run', methods=['POST'])
@cross_origin()
def run():

    code = json.loads(robot_code.get_robot_code(1).code)
    
    # def get_position_by_id(id):
    #     pos = position.Position.query.get(id)
    #     return {
    #         'x': float(pos.x),
    #         'y': float(pos.y), 
    #         'z': float(pos.z)
    #     }
    
    # def get_angles_by_id(id):
    #     pos = position.Position.query.get(id)
    #     return {
    #         'theta1': float(pos.theta1),
    #         'theta2': float(pos.theta2), 
    #         'theta3': float(pos.theta3)
    #     }
    
    def get_full_position_by_id(id):
        pos = position.Position.query.get(id)
        return {
            'theta1': float(pos.theta1),
            'theta2': float(pos.theta2), 
            'theta3': float(pos.theta3),
            'x': float(pos.x),
            'y': float(pos.y), 
            'z': float(pos.z)
        }
    
    # current_position = request.get_json()
    
    current_full_position = motor_monitoring_thread.get_position_and_angles2()
    # current_position_angles = motor_monitoring_thread.get_angles()
    
    movements = []
    sleeps = []
    
    movement = []
    movement.append(current_full_position)
    print(code)
    
    for command in code:
        if command['name'] == 'move_to':
            pos = get_full_position_by_id(int(command['body']))
            
            # pos = position.get_position(int(command['body']))
            
            movement.append(pos)
        if command['name'] == 'sleep':
            movements.append(movement)
            movement = []
            movement.append(movements[-1][-1])
            sleeps.append(int(command['body']))
            movements.append({'sleep': int(command['body'])})
    movements.append(movement)

    print(movements)

    run = calculate_run(movements)
    # run_movement_using_velocities(velocities)
    
    time.sleep(1)
    
    for movement_id, action in run.items():
        if action.get('sleep') is None:
            motor3_thread.send_command({'body': {'velocities': action['velocities']['vtheta3'].tolist(), 'angles': action['angles']['theta3'].tolist()}, 'name': 'move_velocities'})
            motor1_thread.send_command({'body': {'velocities': action['velocities']['vtheta1'].tolist(), 'angles': action['angles']['theta1'].tolist()}, 'name': 'move_velocities'})
            # print('sent move_velocity')
        else:
            motor3_thread.send_command({'name': 'sleep', 'body': int(action['sleep'])})
            motor1_thread.send_command({'name': 'sleep', 'body': int(action['sleep'])})
            # print('sent sleep')

    return {'movements': movements, 'sleeps': sleeps}


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


@app.route('/api/exec-program', methods=['POST'])
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
    
    # with app.app_context():
        # create_tables()
        # program = Command(code='[]')
        # db.session.add(program)
        # db.session.commit()
        
    start_all_threads()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)
