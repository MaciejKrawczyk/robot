from . import db

class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    y = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    z = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    theta1 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    theta2 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    theta3 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)