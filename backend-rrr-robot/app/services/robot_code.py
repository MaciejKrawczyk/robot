from flask_sqlalchemy import SQLAlchemy
from models import RobotCode
import json

    
def get_robot_code(id: int) -> RobotCode:
    robot_code = RobotCode.query.get_or_404(id)
    return robot_code


def update_robot_code(id: int, new_robot_code: str, db_dependency: SQLAlchemy) -> None:
    robot_code = get_robot_code(id)
    robot_code.code = json.dumps(new_robot_code)
    db_dependency.session.commit()