from ..MotorController import MotorController
import time
import threading
from flask_socketio import SocketIO
from queue import Queue
import json
from .MotorHoldingThread import MotorHoldingThread

class MotorThread:
    def __init__(self, socketio_instance: SocketIO, motor_controller: MotorController, id: int, motor_holding_thread: MotorHoldingThread, is_holding_enabled=True) -> None:
        self.motor_controller = motor_controller
        self.command_queue = Queue()
        self.socketio_instance = socketio_instance
        self.id = id
        self.hold_angle = self.motor_controller.get_current_angle()
        self.motor_holding_thread = motor_holding_thread
        self.is_holding_enabled = is_holding_enabled
        

    def _handle_command(self, command):
        name = f'theta{self.id}'
        if command['name'] == f'stop_{name}':
            if self.is_holding_enabled:
                self.motor_holding_thread.start_holding_position()
            # time.sleep(0.01)
            self.motor_controller.stop()
        elif command['name'] == f'{name}+':
            power = command['body']['power']
            if self.is_holding_enabled:
                self.motor_holding_thread.stop_holding_position()
            time.sleep(0.01)
            self.motor_controller.run('plus', power)
        elif command['name'] == f'{name}-':
            power = command['body']['power']
            if self.is_holding_enabled:
                self.motor_holding_thread.stop_holding_position()
            time.sleep(0.01)
            self.motor_controller.run('minus', power)
        elif 'move_velocities' in command['name']: 
            if self.is_holding_enabled:
                self.motor_holding_thread.stop_holding_position()
            time.sleep(0.01)
            self.motor_controller.run_using_pid_control(command['body']['angles'], motor_id=self.id, motor_holding_thread=self.motor_holding_thread, is_last=command['is_last'])
        elif 'sleep' in command['name']:
            if self.is_holding_enabled:
                self.motor_holding_thread.start_holding_position()
            seconds = int(command['body'])
            start_time = time.time()
            print(f'[MOTOR{self.id} SLEEP STARTED] Seconds: {seconds}')
            time.sleep(seconds)
            if self.is_holding_enabled:
                self.motor_holding_thread.stop_holding_position()
            time.sleep(0.01)
            print(f'[MOTOR{self.id} SLEEP FINISHED] Real break time: {time.time() - start_time:.2f}')
    
        
    def _thread_function(self):
        while True:
            command = self.command_queue.get()
            self._handle_command(command)
            time.sleep(0.1)
            # self.motor_controller.start_holding_position()
    
    def start_thread(self):
        self.thread = threading.Thread(target=self._thread_function)
        self.thread.start()
        print('Motor thread started with ID:', self.id)
        
    def send_command(self, command):
        command_json = json.dumps(command)
        commnad_obj = json.loads(command_json)
        self.command_queue.put(commnad_obj)
        
    def get_current_angle(self) -> float:
        return self.motor_controller.get_current_angle()
    