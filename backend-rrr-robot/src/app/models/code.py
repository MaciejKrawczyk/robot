from . import db

class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10000000), nullable=False)