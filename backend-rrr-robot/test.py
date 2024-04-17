from flask import Flask, request
from flask_socketio import SocketIO, emit
import threading
from queue import Queue
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

# Queues for communicating with worker threads
command_queues = [Queue() for _ in range(3)]

# Shared data structure with a lock for monitoring
shared_data = {'thread_statuses': [False, False, False]}
data_lock = threading.Lock()

def worker_thread(thread_id, command_queue):
    while True:
        command = command_queue.get()  # Wait for a command
        if command == "exit":
            break
        # Execute the received command
        print(f"Thread {thread_id}: Executing {command}")
        # Update and emit status when starting the task
        with data_lock:
            shared_data['thread_statuses'][thread_id - 2] = True
            socketio.emit('status_update', {'thread_id': thread_id, 'status': True})
        time.sleep(2)  # Simulate work
        # Update and emit status when task is done
        with data_lock:
            shared_data['thread_statuses'][thread_id - 2] = False
            socketio.emit('status_update', {'thread_id': thread_id, 'status': False})

def monitoring_thread():
    while True:
        with data_lock:
            # Emit the current status periodically
            socketio.emit('status_update', {'all_statuses': shared_data['thread_statuses']})
        time.sleep(1)

@app.route('/command', methods=['POST'])
def send_command():
    data = request.json
    responses = []
    for item in data:
        thread_id = item.get('thread_id', 0)
        command = item.get('command', '')
        if 2 <= thread_id <= 4:
            command_queues[thread_id - 2].put(command)
            responses.append(f"Command '{command}' sent to thread {thread_id}")
        else:
            responses.append(f"Invalid thread ID {thread_id}")
    return "\n".join(responses), 200 if all("Invalid" not in response for response in responses) else 400

if __name__ == "__main__":
    # Start worker threads
    threads = [threading.Thread(target=worker_thread, args=(i, command_queues[i - 2])) for i in range(2, 5)]
    for t in threads:
        t.start()
    
    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitoring_thread)
    monitor_thread.start()

    # Start Flask app with SocketIO support
    socketio.run(app, debug=False, use_reloader=False, host='0.0.0.0')
