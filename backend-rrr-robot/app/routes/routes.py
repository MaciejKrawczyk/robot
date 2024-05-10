from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from controllers import position, code
import time
from utils.plot_generation import plot_all_motor_data



api = Blueprint('api', __name__, url_prefix='/api')


#
# COMMANDS
#

@api.route('/commands/<int:id>', methods=['GET'])
@cross_origin()
def get_command(id: int):
    return code.get_robot_code(id)


@api.route('/commands/<int:id>', methods=['PUT'])
@cross_origin()
def update_command(id):
    return code.update_robot_code(id)


#
# POSITIONS
#

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


#
# PLOT GENERATION
#

# @api.route('/plot', methods=['POST'])
# @cross_origin()
# def plot_motor_data():
#     plot_all_motor_data()
#     return jsonify({'message': 'done'})



@api.route('/exec-program', methods=['POST'])
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
