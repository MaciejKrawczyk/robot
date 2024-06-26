from flask import jsonify, send_file, make_response
import time
from flask_cors import cross_origin
from modules.robot.RRRRobotAPI2 import RobotAPI
from modules.robot.threads.MotorMonitoringThread import MotorMonitoringThread
from modules.robot.threads.MotorThread import MotorThread
from modules.robot.threads.MotorHoldingThread import MotorHoldingThread
import json
from routes.routes import api
from services import position, robot_code
from utils.helpers import calculate_velocity, get_filename_datetime, transform_to_numpy
from utils.plot_generation import plot_angles, plot_positions, plot_angle_velocity, plot_all_motor_data
from utils.bezier_trajectory import bezier, add_points, inverse_kinematics_numpy
from utils.bezier_trajectory_new import robot_trajectory
from app import create_app
from models import position
from config import config
import io
from zipfile import ZipFile
import os
import numpy as np
from types_global import RobotPosition, PointXYZ
from subprocess import call



app, socketio = create_app()
app.register_blueprint(api)

robotAPI = RobotAPI()

motor1_controller = robotAPI.motor1_controller
motor2_controller = robotAPI.motor2_controller 
motor3_controller = robotAPI.motor3_controller

motor1_holding_thread = MotorHoldingThread(socketio, motor1_controller, 1)
motor2_holding_thread = MotorHoldingThread(socketio, motor2_controller, 2)
motor3_holding_thread = MotorHoldingThread(socketio, motor3_controller, 3)

motor1_thread = MotorThread(socketio, motor1_controller, 1, motor1_holding_thread, is_holding_enabled=True)
motor2_thread = MotorThread(socketio, motor2_controller, 2, motor2_holding_thread, is_holding_enabled=True)  
motor3_thread = MotorThread(socketio, motor3_controller, 3, motor3_holding_thread, is_holding_enabled=True)
motor_monitoring_thread = MotorMonitoringThread(
    socketio,
    motor1_controller=motor1_controller, 
    motor2_controller=motor2_controller,
    motor3_controller=motor3_controller
)

def calculate_run(movements):
    
    cnt = 1
    step = 0.01
    
    run = {}
    last_index = len(movements) - 1  # Calculate the last index of the movements list
    for movement_id, movement in enumerate(movements):
        
        if not isinstance(movement, dict):
            
            run[movement_id] = {'velocities': {'vtheta1': [], 'vtheta2': [], 'vtheta3': []}, 'angles': {'theta1': [], 'theta2': [], 'theta3': []}}
            

            
            point1 = PointXYZ(movement[0].x, movement[0].y, movement[0].z)
            point2 = PointXYZ(movement[1].x, movement[1].y, movement[1].z)
            
            # numpy_notation_movement_list = transform_to_numpy(movement)

            # X, Y, Z = add_points(numpy_notation_movement_list, cnt)
            
            # x, y, z, theta1, theta2, theta3 = bezier(X, Y, Z, step)
            
            
            
            
            x, y, z, theta1, theta2, theta3 = robot_trajectory(point1, point2)
            print(x)
            print(y)

            # vtheta1, vtheta2, vtheta3 = calculate_velocity(theta1, theta2, theta3, step)

            # total_time = len(x) * step
            # plot_angles(
            #     theta1, theta2, theta3,
            #     total_time,
            #     f'calculated_motor_plots/{get_filename_datetime()}_movement_{movement_id}_angles_over_time_calculated'
            # )
            # plot_positions(
            #     x, y, z,
            #     total_time,
            #     f'calculated_motor_plots/{get_filename_datetime()}_movement_{movement_id}_position_over_time_calculated'
            # )
            # plot_angle_velocity(
            #     vtheta1, vtheta2, vtheta3,
            #     step, 
            #     f'calculated_motor_plots/{get_filename_datetime()}_movement_{movement_id}_angle_velocity_over_time_calculated'
            # )

            run[movement_id]['velocities']['vtheta1'] = []
            run[movement_id]['velocities']['vtheta2'] = []
            run[movement_id]['velocities']['vtheta3'] = []
            run[movement_id]['angles']['theta1'] = theta1
            run[movement_id]['angles']['theta2'] = theta2
            run[movement_id]['angles']['theta3'] = theta3
            run[movement_id]['is_last'] = (movement_id == last_index)
            
        else:
            run[movement_id] = {'sleep': movement['sleep']}
        # continue
    
    return run



@app.route('/api/plot', methods=['POST'])
def download_images():
    plot_all_motor_data()
    return {"message": "ok"}


@app.route('/api/turnoff', methods=['POST'])
def exit():
    response = call(['/home/maciek/Desktop/robot/backend-rrr-robot/app/shutdown.sh'])
    if response == 0:
        return {"message": "Shutdown initiated successfully."}
    else:
        return {"message": "Failed to initiate shutdown."}, 500


@app.route('/api/stop', methods=['POST'])
@cross_origin()
def stop_run():
    motor1_thread.send_command({"name": "stop_theta1"})
    motor2_thread.send_command({"name": "stop_theta2"})
    motor3_thread.send_command({"name": "stop_theta3"})
    return {"message": "run stopped"}


@app.route('/api/run', methods=['POST'])
@cross_origin()
def run():

    code = json.loads(robot_code.get_robot_code(1).code)
    
    def get_full_position_by_id(id):
        pos = position.Position.query.get(id)
        robot_position = RobotPosition(float(pos.theta1), float(pos.theta2), float(pos.theta3), float(pos.x), float(pos.y), float(pos.z))
        # return {
        #     'theta1': float(pos.theta1),
        #     'theta2': float(pos.theta2), 
        #     'theta3': float(pos.theta3),
        #     'x': float(pos.x),
        #     'y': float(pos.y), 
        #     'z': float(pos.z)
        # }
        return robot_position
    
    current_full_position = motor_monitoring_thread.get_position_and_angles2()
    
    movements = []
    sleeps = []
    
    movement = []
    movement.append(current_full_position)
    
    for command in code:
        if command['name'] == 'move_to':
            pos = get_full_position_by_id(int(command['body']))
            movement.append(pos)
            
        if command['name'] == 'sleep':
            movements.append(movement)
            movement = []
            movement.append(movements[-1][-1])
            sleeps.append(float(command['body']))
            movements.append({'sleep': float(command['body'])})
            
    movements.append(movement)

    print(movements)

    run = calculate_run(movements)
    
    time.sleep(1)
    
    for movement_id, action in run.items():
        
    
        if action.get('sleep') is not None:
            motor3_thread.send_command({'name': 'sleep', 'body': int(action['sleep'])})
            motor2_thread.send_command({'name': 'sleep', 'body': int(action['sleep'])})
            motor1_thread.send_command({'name': 'sleep', 'body': int(action['sleep'])})
        else:
            # motor3_thread.send_command({'body': {'velocities': action['velocities']['vtheta3'].tolist(), 'angles': action['angles']['theta3'].tolist()}, 'name': 'move_velocities', 'is_last': action['is_last']})
            # motor2_thread.send_command({'body': {'velocities': action['velocities']['vtheta2'].tolist(), 'angles': action['angles']['theta2'].tolist()}, 'name': 'move_velocities', 'is_last': action['is_last']})
            # motor1_thread.send_command({'body': {'velocities': action['velocities']['vtheta1'].tolist(), 'angles': action['angles']['theta1'].tolist()}, 'name': 'move_velocities', 'is_last': action['is_last']})
            motor3_thread.send_command({'body': {'velocities': action['velocities']['vtheta3'], 'angles': action['angles']['theta3']}, 'name': 'move_velocities', 'is_last': action['is_last']})
            motor2_thread.send_command({'body': {'velocities': action['velocities']['vtheta2'], 'angles': action['angles']['theta2']}, 'name': 'move_velocities', 'is_last': action['is_last']})
            motor1_thread.send_command({'body': {'velocities': action['velocities']['vtheta1'], 'angles': action['angles']['theta1']}, 'name': 'move_velocities', 'is_last': action['is_last']})


    return {'movements': movements, 'sleeps': sleeps}



##
## socket
##

@socketio.on('send-command')
def handle_command(command_object):
    
    available_commands = ['theta1+', 'theta1-', 'theta2+', 'theta2-', 'theta3+', 'theta3-', 'stop_theta1', 'stop_theta2', 'stop_theta3']

    command_name = command_object['name']
    command_body = command_object['body']

    if command_name not in available_commands:
        return jsonify({"error": "command is not available!"})

    match command_name:
        case 'stop_theta1':
            motor1_thread.send_command(command_object)
        case 'stop_theta2':
            motor2_thread.send_command(command_object)
        case 'stop_theta3':
            motor3_thread.send_command(command_object)
        case 'theta1+':
            motor1_thread.send_command(command_object)
        case 'theta1-':
            motor1_thread.send_command(command_object)
        case 'theta2+':
            motor2_thread.send_command(command_object)
        case 'theta2-':
            motor2_thread.send_command(command_object)
        case 'theta3+':
            motor3_thread.send_command(command_object)
        case 'theta3-':
            motor3_thread.send_command(command_object)
        # case _:
        
    print(f'received command: {command_object}')



def start_all_threads():
    motor1_thread.start_thread()
    motor2_thread.start_thread()
    motor3_thread.start_thread()
    motor_monitoring_thread.start_thread()
    
    if config['ENABLE_HOLDING_THREAD']:
        motor1_holding_thread.start_thread()
        motor2_holding_thread.start_thread()
        motor3_holding_thread.start_thread()
    
    print('started all threads...')


if __name__ == '__main__':
    
    # with app.app_context():
        # create_tables()
        # program = Command(code='[]')
        # db.session.add(program)
        # db.session.commit()
        
    start_all_threads()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False, allow_unsafe_werkzeug=True)
