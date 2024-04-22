from services import position
from flask import jsonify, request
import json
from app import db
from types_global import RobotPosition


db_dependency = db


def post_position():
    body = request.get_json()
    new_position = RobotPosition(
        x = body['x'],
        y = body['y'],
        z = body['z'],
        theta1 = body['theta1'],
        theta2 = body['theta2'],
        theta3 = body['theta3'],
    )
    position.save_position(new_position, db_dependency)
    return jsonify({'message': 'position created'})


def get_positions():
    positions = position.get_positions()
    return jsonify([{
        'id': pos.id,
        'x': float(pos.x),
        'y': float(pos.y),
        'z': float(pos.z),
        'theta1': float(pos.theta1),
        'theta2': float(pos.theta2),
        'theta3': float(pos.theta3)
    } for pos in positions])


def get_position(id:int):
    fetched_position = position.get_position(id)
    return jsonify({
        'id': fetched_position.id,
        'x': float(fetched_position.x),
        'y': float(fetched_position.y),
        'z': float(fetched_position.z),
        'theta1': float(fetched_position.theta1),
        'theta2': float(fetched_position.theta2),
        'theta3': float(fetched_position.theta3)
    })


def delete_position(id: int):
    try:
        position.delete_position(id, db_dependency)
        return jsonify({
            'message': 'successfully deleted'
        }), 200
    except:
        return jsonify({
            'message': 'not found'
        }), 404