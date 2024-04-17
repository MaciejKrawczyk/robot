from MotorController import MotorController
import time
import threading
from flask_socketio import SocketIO
from queue import Queue
import json

class MotorThread:
    def __init__(self, socketio_instance: SocketIO, motor_controller: MotorController, id: int) -> None:
        self.motor_controller = motor_controller
        self.command_queue = Queue()
        self.socketio_instance = socketio_instance
        self.id = id

    def _handle_command(self, command: str):
        name = f'theta{self.id}'
        if command == f'stop_{name}':
            self.motor_controller.stop()
        elif command == f'{name}+':
            self.motor_controller.run('plus')
        elif command == f'{name}-':
            self.motor_controller.run('minus')
        # here should be advanced logic for handling commands

    def thread_function(self):
        socketio_instance = self.socketio_instance
        while True:
            command = self.command_queue.get()
            self._handle_command(command)
            time.sleep(0.1)
    
    def start_thread(self):
        self.thread = threading.Thread(target=self.thread_function)
        self.thread.start()
        print('Motor thread started with ID:', self.id)
        
    def send_command(self, command):
        command_json = json.dumps(command)
        commnad_obj = json.loads(command_json)
        self.command_queue.put(commnad_obj)