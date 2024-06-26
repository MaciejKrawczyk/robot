from .MotorEncoderCombo_i2c import MotorEncoderCombo_i2c
import time
import matplotlib.pyplot as plt
import datetime
import os

PULSES_PER_REVOLUTION = 1250

def get_filename_datetime():
    # Current date and time
    now = datetime.datetime.now()
    # Format as a string suitable for filenames
    formatted = now.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted



class MotorController:
    def __init__(self, motor: MotorEncoderCombo_i2c, id, is_holding_enabled=True):
        self.id = id
        self.motor = motor
        self.Kp = 8.1
        self.Ki = 0.47
        self.Kd = 0.15
        self.target_angle = self.get_current_angle()
        self.holding_position = True
        self.is_holding_position_enabled = is_holding_enabled

    def get_current_angle(self):
        return self.motor.get_angle()

    def run(self, direction, percent_of_power=50):
        if self.is_holding_position_enabled:
            self.stop_holding_position()
        self.motor.run_motor(direction=direction, percent_of_power=percent_of_power)

    def start_holding_position(self, motor_id=''):
        self.target_angle = self.get_current_angle()
        self.holding_position = True
        print(f'[MOTOR {motor_id}] HOLDING POSITION: {round(self.target_angle, 2)}°')
        self.hold_position()

    def stop_holding_position(self, motor_id=''):
        print(f'[MOTOR {motor_id}] HOLDING POSITION STOPPED!')
        self.holding_position = False

    def stop(self):
        self.motor.stop()

    def sleep(self, seconds, motor_id=''):
        if self.is_holding_position_enabled:
            self.start_holding_position()
        start_time = time.time()  # Start time for reference
        print(f'[MOTOR{motor_id} SLEEP STARTED] Seconds: {seconds}')
        time.sleep(seconds)
        if self.is_holding_position_enabled:
            self.stop_holding_position()
        print(f'[MOTOR{motor_id} SLEEP FINISHED] Real break time: {time.time() - start_time:.2f}')


    def hold_position(self):
        Kp = self.Kp
        Ki = self.Ki
        Kd = self.Kd

        prev_error = 0
        integral = 0
        error_threshold = 0.65  # Set the threshold value below which no adjustment is made

        while self.holding_position:
            current_angle = self.motor.get_angle()
            error = self.target_angle - current_angle

            # Only adjust if the error is greater than the threshold
            if abs(error) > error_threshold:
                integral += error * 0.01
                derivative = (error - prev_error) / 0.01
                prev_error = error

                pid_output = Kp * error + Ki * integral + Kd * derivative

                direction = 'plus' if pid_output > 0 else 'minus'
                speed_percentage = max(20, min(100, abs(pid_output)))

                self.motor.run_motor(direction, speed_percentage)
            else:
                self.motor.stop()
                prev_error = error
            
            # if self.id == 3:
                # print(error)
                
            time.sleep(0.01)


    def run_using_pid_control(self, target_angles, motor_holding_thread, motor_id='', is_last=False):
        if self.is_holding_position_enabled:
            self.stop_holding_position()

        directory = 'motor_data'
        os.makedirs(directory, exist_ok=True)
        
        print(f'[MOTOR{motor_id} MOVEMENT STARTED] Movement in progress...')
        start_time = time.time()

        times = []
        actual_angles = []
        target_angles_record = []
        pid_outputs = []
        errors = []

        Kp = self.Kp
        Ki = self.Ki
        Kd = self.Kd

        prev_error = 0
        integral = 0

        for target_angle in target_angles:
            current_angle = self.motor.get_angle()
            error = target_angle - current_angle
            errors.append(error)

            integral += error * 0.01
            derivative = (error - prev_error) / 0.01
            prev_error = error

            pid_output = Kp * error + Ki * integral + Kd * derivative
            pid_outputs.append(pid_output)

            direction = 'plus' if pid_output > 0 else 'minus'
            speed_percentage = max(20, min(100, abs(pid_output)))

            self.motor.run_motor(direction, speed_percentage)

            current_time = time.time() - start_time
            times.append(current_time)
            actual_angles.append(current_angle)
            target_angles_record.append(target_angle)

            time.sleep(0.01)

        self.motor.stop()
        
        elapsed_time = time.time() - start_time
        print(f"[MOTOR{motor_id} FINISHED MOVEMENT] Total runtime: {elapsed_time:.2f} seconds")

        # Calculate mean square error
        mse = sum((ta - aa) ** 2 for ta, aa in zip(target_angles_record, actual_angles)) / len(target_angles_record)

        # Save data to a text file within the directory
        filename = os.path.join(directory, f"{get_filename_datetime()}_motor{motor_id}_data.txt")
        with open(filename, 'w') as file:
            # file.write(f"Time,ActualAngle,TargetAngle,PIDOutput,Error\n")
            for time_point, actual_angle, target_angle, pid_output, error in zip(times, actual_angles, target_angles_record, pid_outputs, errors):
                file.write(f"{time_point},{actual_angle},{target_angle},{pid_output},{error}\n")
            # file.write(f"\nMean Square Error: {mse}\n")

        if is_last:
            if self.is_holding_position_enabled:
                # self.start_holding_position()
                motor_holding_thread.start_holding_position()


    def run_using_velocities_array_no_pid(self, velocities, target_angles, motor_id=''):
        print(f'[MOTOR{motor_id} MOVEMENT STARTED] Movement in progress...')
        start_time = time.time()

        times = []
        actual_angles = []
        actual_velocities = []

        for velocity in velocities:
            try:
                if velocity > 0:
                    direction = 'plus'
                else:
                    direction = 'minus'

                # Calculate speed percentage with a minimum of 20 and a maximum of 100
                speed_percentage = max(20, min(100, abs(velocity)))

                # Run the motor with the given speed
                self.motor.run_motor(direction, speed_percentage)
                actual_velocities.append(speed_percentage)

                current_time = time.time() - start_time
                current_angle = self.motor.get_angle()

                # Record time and angle
                times.append(current_time)
                actual_angles.append(current_angle)

                # Small delay to prevent hogging the CPU
                time.sleep(0.01)

            except Exception as e:
                print(f"Error: {e}")
                self.motor.stop()
                break

        # Stop the motor after finishing the velocity array
        self.motor.stop()
        elapsed_time = time.time() - start_time
        print(f"[MOTOR{motor_id} FINISHED MOVEMENT] Total runtime: {elapsed_time:.2f} seconds")

        # Plotting the motor angle over time with target angles
        plt.figure(figsize=(10, 5))
        plt.plot(times, actual_angles, label='Actual Motor Angle', marker='o')
        plt.plot(times, target_angles, label='Target Motor Angle', linestyle='--')
        plt.title(f'Motor{motor_id} Angle Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Motor Angle (degrees)')
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{get_filename_datetime()}_motor{motor_id}_angles.png")
        plt.show()

        # Plotting the commanded velocities over time
        plt.figure(figsize=(10, 5))
        plt.plot(times, actual_velocities, label='Commanded Velocities', marker='o')
        plt.title(f'Motor{motor_id} Velocity Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Velocity (%)')
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{get_filename_datetime()}_motor{motor_id}_velocities.png")
        plt.show()


    def run_using_velocities_array(self, velocities, target_angles, motor_id=''):
        print(f'[MOTOR{motor_id} MOVEMENT STARTED] Movement in progress...')
        start_time = time.time()

        # Initialize PID variables
        integral = 0
        previous_error = 0

        times = []
        actual_angles = []
        actual_velocities = []
        measured_velocities = []

        for velocity, target_angle in zip(velocities, target_angles):
            try:
                if velocity > 0:
                    direction = 'plus'
                else:
                    direction = 'minus'

                speed_percentage = max(0, min(100, abs(velocity)))

                # Run the motor at the start to set initial movement
                self.motor.run_motor(direction, speed_percentage)
                actual_velocities.append(speed_percentage)

                current_time = time.time() - start_time
                current_angle = self.motor.get_angle()

                # PID calculation
                error = target_angle - current_angle
                integral += error * 0.01  # Assuming time step of 0.01 seconds
                derivative = (error - previous_error) / 0.01
                output = self.Kp * error + self.Ki * integral + self.Kd * derivative

                # Adjust the motor speed based on PID output
                adjusted_speed = max(0, min(100, abs(output)))
                self.motor.run_motor(direction, adjusted_speed)
                measured_velocities.append(adjusted_speed)

                # Record time and angle
                times.append(current_time)
                actual_angles.append(current_angle)

                # Update previous error
                previous_error = error

                # Small delay to prevent hogging the CPU
                time.sleep(0.01)

            except Exception as e:
                print(f"Error: {e}")
                self.motor.stop()
                break

        # Stop the motor after finishing the velocity array
        self.motor.stop()
        elapsed_time = time.time() - start_time
        print(f"[MOTOR{motor_id} FINISHED MOVEMENT] Total runtime: {elapsed_time:.2f} seconds")
        
        # Plotting the motor angle over time with target angles
        plt.figure(figsize=(10, 5))
        plt.plot(times, actual_angles, label='Actual Motor Angle', marker='o')
        plt.plot(times, target_angles, label='Target Motor Angle', linestyle='--')
        plt.title(f'Motor{motor_id} Angle Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Motor Angle (degrees)')
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{get_filename_datetime()}_motor{motor_id}_angles.png")
        plt.show()

        # Plotting the actual vs adjusted velocities
        plt.figure(figsize=(10, 5))
        plt.plot(times, actual_velocities, label='Commanded Velocities', marker='o')
        plt.plot(times, measured_velocities, label='Actual Velocities', linestyle='--')
        plt.title(f'Motor{motor_id} Velocity Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Velocity (%)')
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{get_filename_datetime()}_motor{motor_id}_velocities.png")
        plt.show()


    def move_to(self, angle, hold=False):
        current_angle = self.motor.get_angle()

        # PID constants
        Kp = 0.1
        Ki = 0.1
        Kd = 0

        acceptable_error_margin = 0.2  # Define an acceptable error margin

        integral = 0.0
        previous_error = 0.0

        start_time = time.time()
        ramp_duration = 0  # Initially, no ramp-up period
        initial_power = 20
        ramp_end_time = time.time() + ramp_duration

        while True:
            current_angle = self.motor.get_angle()
            error = angle - current_angle

            # PID calculations
            P = error
            integral += error * 0.01  # Assuming loop time of 0.01 seconds
            I = integral
            D = (error - previous_error) / 0.01  # Derivative of error
            
            pid_power = Kp * P + Ki * I + Kd * D

            if time.time() < ramp_end_time:
                power_percent = initial_power + (pid_power - initial_power) * ((time.time() - start_time) / ramp_duration)
            else:
                power_percent = pid_power

            power_percent = max(20, min(100, power_percent))  # Limit the power_percent to be within 20-100%

            # Direction handling
            direction = 'minus' if error > 0 else 'plus'
            self.motor.run_motor(direction, abs(power_percent))

            if hold and abs(error) <= acceptable_error_margin:
                self.motor.stop()
                break  # Exit the loop if holding and error is within the margin
            elif not hold and abs(error) < acceptable_error_margin:
                self.motor.stop()
                break  # Also exit the loop if not holding and error is small enough

            time.sleep(0.01)  # Small delay to prevent hogging the CPU

            previous_error = error

        
        # # Plotting the angle data
        # plt.plot(time_data, angle_data)
        # plt.xlabel('Time (s)')
        # plt.ylabel('Angle (degrees)')
        # plt.title('Angle Change Over Time')

        # plt.grid(True)  

        # # Save the plot as an image file
        # plt.savefig(f'angle_plot_{time.time()}.png')

        # # Close the plot
        # plt.close()