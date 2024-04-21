from app import db

class RobotCode(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10000000), nullable=False)