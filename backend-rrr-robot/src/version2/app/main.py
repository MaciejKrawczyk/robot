from flask import Flask, jsonify, request
import time
from flask_socketio import SocketIO
from flask_cors import CORS
from RRRRobotAPI2 import RobotAPI
from threads.MotorMonitoringThread import MotorMonitoringThread
from threads.MotorThread import MotorThread
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
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
    name = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(80), nullable=False)
    
class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    y = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    z = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    theta1 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    theta2 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    theta3 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

@app.route('/commands', methods=['POST'])
def create_command():
    data = request.get_json()
    command = Command(name=data['name'], body=data['body'] )
    db.session.add(command)
    db.session.commit()
    return jsonify({'message': 'Command created'}), 201

@app.route('/commands', methods=['GET'])
def get_commands():
    commands = Command.query.all()
    return jsonify([{'id': command.id, 'name': command.name, 'body': command.body} for command in commands])

@app.route('/commands/<int:id>', methods=['GET'])
def get_command(id):
    command = Command.query.get_or_404(id)
    return jsonify({'id': command.id, 'name': command.name, 'body': command.body})

@app.route('/commands/<int:id>', methods=['PUT'])
def update_command(id):
    data = request.get_json()
    command = Command.query.get_or_404(id)
    command.name = data['name']
    command.body = data['body']
    db.session.commit()
    return jsonify({'message': 'Command updated'})

@app.route('/commands/<int:id>', methods=['DELETE'])
def delete_command(id):
    command = Command.query.get_or_404(id)
    db.session.delete(command)
    db.session.commit()
    return jsonify({'message': 'Command deleted'})

@app.route('/positions', methods=['POST'])
def create_position():
    data = request.get_json()
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
    with app.app_context():
        create_tables()
    start_all_threads()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
