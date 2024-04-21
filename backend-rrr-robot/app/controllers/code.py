from services import robot_code
from flask import jsonify, request
from app import db


db_dependency = db


def get_robot_code(id: int):
    fetched_robot_code = robot_code.get_robot_code(id=id)
    return jsonify(
        {
            'id': fetched_robot_code.id, 
            'code': fetched_robot_code.code
        }
    )


def update_robot_code(id: int):
    body = request.get_json()
    robot_code.update_robot_code(id, body['code'], db_dependency)
    return jsonify({'message': 'code updated'})