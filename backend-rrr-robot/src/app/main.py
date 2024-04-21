from flask import Flask, jsonify, request
import time
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
from RRRRobotAPI2 import RobotAPI
from threads.MotorMonitoringThread import MotorMonitoringThread
from threads.MotorThread import MotorThread
from flask_sqlalchemy import SQLAlchemy
import json
import numpy as np
from utils import add_points, bezier, calculate_velocity, plot_positions, plot_velocity, plot_velocity_with_calculated_velocitites, get_filename_datetime, modify_curve, plot_angles, shortest_path
from kinematics_utils import inverse_kinematics3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
db = SQLAlchemy(app)

def create_tables():
    db.create_all()

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
## crud
##

class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10000000), nullable=False)
    
class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    y = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    z = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    theta1 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    theta2 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    theta3 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)


def transform_to_numpy(points):
    # Extract x, y, z coordinates into separate lists
    x_coords = [point['x'] for point in points]
    y_coords = [point['y'] for point in points]
    z_coords = [point['z'] for point in points]
    
    # Stack these lists vertically into a NumPy array
    numpy_array = np.array([x_coords, y_coords, z_coords])
    
    return numpy_array


def calculate_run(movements):
    
    cnt = 0.5
    step = 0.01
    
    run = {}
    for movement_id, movement in enumerate(movements):
        
        if not isinstance(movement, dict):
        
            run[movement_id] = {'velocities': {'vtheta1': [], 'vtheta2': [], 'vtheta3': []}, 'angles': {'theta1': [], 'theta2': [], 'theta3': []}}
            
            numpy_notation_movement_list = transform_to_numpy(movement)
            # print(f'calculating points, cnt = {cnt}')
            X, Y, Z = add_points(numpy_notation_movement_list, cnt)
            # print(f'calculating trajectory, step = {step}s')
            # x_b, y_b, z_b = bezier(X, Y, Z, step)
            
            x, y, z, theta1, theta2, theta3 = bezier(X, Y, Z, step)
            
            # x, y, z, theta1, theta2, theta3 = shortest_path(X, Y, Z, step)
            
            # print(x_b)
            # x, y, z = modify_curve(x_b, y_b, z_b, inverse_kinematics3)  #TODO need to be changed to theta1, theta2, theta3
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
            plot_velocity_with_calculated_velocitites(
                x, vtheta1, vtheta2, vtheta3,
                step, 
                f'{get_filename_datetime()}_movement_{movement_id}_velocity_over_time_calculated'
            )

            run[movement_id]['velocities']['vtheta1'] = vtheta1
            run[movement_id]['velocities']['vtheta2'] = vtheta2
            run[movement_id]['velocities']['vtheta3'] = vtheta3
            run[movement_id]['angles']['theta1'] = theta1
            run[movement_id]['angles']['theta2'] = theta2
            run[movement_id]['angles']['theta3'] = theta3
            
        else:
            run[movement_id] = {'sleep': movement['sleep']}
    
    print(run)
    return run


@app.route('/run', methods=['POST'])
@cross_origin()
def run():

    code = json.loads(Command.query.get_or_404(1).code)
    
    def get_position_by_id(id):
        position = Position.query.get(id)
        return {
            'x': float(position.x),
            'y': float(position.y), 
            'z': float(position.z)
            }
    
    current_position = request.get_json()
    
    movements = []
    sleeps = []
    
    movement = []
    movement.append(current_position)
    
    
    for command in code:
        if command['name'] == 'move_to':
            position = get_position_by_id(int(command['body']))
            movement.append(position)
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


@app.route('/commands/<int:id>', methods=['GET'])
@cross_origin()
def get_command(id):
    command = Command.query.get_or_404(id)
    return jsonify({'id': command.id, 'code': command.code})

@app.route('/commands/<int:id>', methods=['PUT'])
@cross_origin()
def update_command(id):
    data = request.get_json()
    command = Command.query.get_or_404(id)
    command.code = json.dumps(data['code'])
    db.session.commit()
    return jsonify({'message': 'Command updated'})

@app.route('/positions', methods=['POST'])
@cross_origin()
def create_position():
    data = request.get_json()
    print(data)
    position = Position(
        x=data['x'],
        y=data['y'],
        z=data['z'],
        theta1=data['theta1'],
        theta2=data['theta2'],
        theta3=data['theta3']
    )
    db.session.add(position)
    db.session.commit()
    return jsonify({'message': 'Position created'}), 201

@app.route('/positions', methods=['GET'])
@cross_origin()
def get_positions():
    positions = Position.query.all()
    return jsonify([{
        'id': pos.id,
        'x': float(pos.x),
        'y': float(pos.y),
        'z': float(pos.z),
        'theta1': float(pos.theta1),
        'theta2': float(pos.theta2),
        'theta3': float(pos.theta3)
    } for pos in positions])

@app.route('/positions/<int:id>', methods=['GET'])
@cross_origin()
def get_position(id):
    position = Position.query.get_or_404(id)
    return jsonify({
        'id': position.id,
        'x': float(position.x),
        'y': float(position.y),
        'z': float(position.z),
        'theta1': float(position.theta1),
        'theta2': float(position.theta2),
        'theta3': float(position.theta3)
    })

@app.route('/positions/<int:id>', methods=['PUT'])
@cross_origin()
def update_position(id):
    data = request.get_json()
    position = Position.query.get_or_404(id)
    position.x = data['x']
    position.y = data['y']
    position.z = data['z']
    position.theta1 = data['theta1']
    position.theta2 = data['theta2']
    position.theta3 = data['theta3']
    db.session.commit()
    return jsonify({'message': 'Position updated'})

@app.route('/positions/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_position(id):
    position = Position.query.get_or_404(id)
    db.session.delete(position)
    db.session.commit()
    return jsonify({'message': 'Position deleted'})


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
    
    with app.app_context():
        create_tables()
        program = Command(code='[]')
        db.session.add(program)
        db.session.commit()
        
    start_all_threads()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)
