#!/bin/bash

# Start the npm server
cd ~/Desktop/robot/frontend-rrr-robot || exit 1
npm run dev > ~/Desktop/robot/npm_out.log 2> ~/Desktop/robot/npm_err.log &
NPM_PID=$!

# Wait for npm server to start successfully (adjust the sleep duration as needed)
sleep 5

# Navigate to the Python server directory
cd ~/Desktop/robot/backend-rrr-robot
export PYTHONPATH=/home/maciek/Desktop/robot/backend-rrr-robot
source .venv/bin/activate
python3 app/main.py > ~/Desktop/robot/flask_out.log 2> ~/Desktop/robot/flask_err.log &

# Optionally wait for Python server to start (adjust sleep as needed)
sleep 5

# No need to bring the npm process back to the foreground
# fg %1  # Commented out as it's usually not required

# Wait for the NPM process to finish
wait $NPM_PID
