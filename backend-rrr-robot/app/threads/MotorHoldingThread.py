from MotorController import MotorController
import time
import threading
from flask_socketio import SocketIO
from queue import Queue
import json

class MotorHoldingThread:
    def __init__(self, socketio_instance: SocketIO, motor_controller: MotorController, id: int) -> None:
        self.motor_controller = motor_controller
        self.command_queue = Queue()
        self.socketio_instance = socketio_instance
        self.id = id
        self.hold_angle = self.motor_controller.get_current_angle()
        self.name = f'theta{self.id}'

    def start_holding_position(self):
        # self.motor_controller.start_holding_position()
        self.command_queue.put(f'start_holding')
        print('motor_holding_thread: sent "start_holding"')
        
    def stop_holding_position(self):
        self.command_queue.put(f'stop_holding')
        print('motor_holding_thread: sent "stop_holding"')
        # self.motor_controller.stop_holding_position()

    def _handle_command(self, command: str):
        if command == f'stop_holding':
            print('received "stop_holding" in _handle_command')
            self.motor_controller.stop_holding_position(motor_id=self.id)
        
        elif command == f'start_holding':
            print('received "start_holding" in _handle_command')
            self.motor_controller.start_holding_position(motor_id=self.id)
        
        
    def _thread_function(self):
        # self.start_holding_position()
        while True:
            command = self.command_queue.get()
            self._handle_command(command)
            time.sleep(0.1)
            # self.motor_controller.start_holding_position()
    
    def start_thread(self):
        self.thread = threading.Thread(target=self._thread_function)
        self.thread.start()
        print('Motor holding thread started with ID:', self.id)
        self.start_holding_position()
        print(f'motor_holding_thread id: {self.id} started holding')
    