from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from controllers import position, code
import time



api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/commands/<int:id>', methods=['GET'])
@cross_origin()
def get_command(id: int):
    return code.get_robot_code(id)


@api.route('/commands/<int:id>', methods=['PUT'])
@cross_origin()
def update_command(id):
    return code.update_robot_code(id)


@api.route('/positions', methods=['POST'])
@cross_origin()
def create_position():
    return position.post_position()
    

@api.route('/positions', methods=['GET'])
@cross_origin()
def get_positions():
    return position.get_positions()


@api.route('/positions/<int:id>', methods=['GET'])
@cross_origin()
def get_position(id):
    return position.get_position(id)

@api.route('/positions/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_position(id):
    id = int(id)
    return position.delete_position(id)


@api.route('api/exec-program', methods=['POST'])
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
                
                
# @api.route('/run', methods=['POST'])
# @cross_origin()
# def run():

#     code = json.loads(Command.query.get_or_404(1).code)
    
#     def get_position_by_id(id):
#         position = Position.query.get(id)
#         return {
#             'x': float(position.x),
#             'y': float(position.y), 
#             'z': float(position.z)
#             }
    
#     current_position = request.get_json()
    
#     movements = []
#     sleeps = []
    
#     movement = []
#     movement.append(current_position)
    
    
#     for command in code:
#         if command['name'] == 'move_to':
#             position = get_position_by_id(int(command['body']))
#             movement.append(position)
#         if command['name'] == 'sleep':
#             movements.append(movement)
#             movement = []
#             movement.append(movements[-1][-1])
#             sleeps.append(int(command['body']))
#             movements.append({'sleep': int(command['body'])})
#     movements.append(movement)

#     print(movements)

#     run = calculate_run(movements)
#     # run_movement_using_velocities(velocities)
    
#     for movement_id, action in run.items():
#         if action.get('sleep') is None:
#             motor3_thread.send_command({'body': {'velocities': action['velocities']['vtheta3'].tolist(), 'angles': action['angles']['theta3'].tolist()}, 'name': 'move_velocities'})
#             motor1_thread.send_command({'body': {'velocities': action['velocities']['vtheta1'].tolist(), 'angles': action['angles']['theta1'].tolist()}, 'name': 'move_velocities'})
#             # print('sent move_velocity')
#         else:
#             motor3_thread.send_command({'name': 'sleep', 'body': int(action['sleep'])})
#             motor1_thread.send_command({'name': 'sleep', 'body': int(action['sleep'])})
#             # print('sent sleep')

#     return {'movements': movements, 'sleeps': sleeps}

