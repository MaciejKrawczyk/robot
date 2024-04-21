from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key_here'
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    socketio = SocketIO(app, cors_allowed_origins="*")
    CORS(app)    

    db.init_app(app)
    
    def create_tables():
        db.create_all()

    from .models import robot_code, position
    from .routes import routes
    from .controllers import code, position
    
    with app.app_context():
        create_tables()
        program = robot_code.RobotCode(code='[]')
        db.session.add(program)
        db.session.commit()
    
    return app, socketio