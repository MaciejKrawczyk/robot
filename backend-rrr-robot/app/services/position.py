from types_global import RobotPosition
from models import Position
from typing import List

def save_position(new_position: RobotPosition, db_dependency) -> None:
    position = Position(
        x = new_position.x,
        y = new_position.y,
        z = new_position.z,
        theta1 = new_position.theta1,
        theta2 = new_position.theta2,
        theta3 = new_position.theta3
    )
    db_dependency.session.add(position)
    db_dependency.session.commit()
    
    
def get_positions() -> List[Position]:
    positions = Position.query.all()
    return positions


def get_position(id: int) -> Position:
    position = Position.query.get_or_404(id)
    return position

def delete_position(id: int, db_dependency) -> None:
    position = get_position(id)
    try:
        db_dependency.session.delete(position)
        db_dependency.session.commit()
    except:
       raise ValueError('not found') 