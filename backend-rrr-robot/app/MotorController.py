from MotorEncoderCombo import MotorEncoderCombo
import time
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import datetime

PULSES_PER_REVOLUTION = 1250

def get_filename_datetime():
    # Current date and time
    now = datetime.datetime.now()
    # Format as a string suitable for filenames
    formatted = now.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted


class MotorController:
    def __init__(self, motor: MotorEncoderCombo):
        self.motor = motor
        self.Kp = 1.0  # Proportional gain
        self.Ki = 0.1  # Integral gain
        self.Kd = 0.05 # Derivative gain

    def get_current_angle(self):
        return self.motor.get_angle()

    def set_angle_to(self, angle):
        pass

    def increment_angle_by(self, angle):
        pass

    def run(self, direction, percent_of_power=100):
        self.motor.run_motor(direction=direction, percent_of_power=percent_of_power)

    def stop(self):
        self.motor.stop()

    def sleep(self, seconds, motor_id=''):
        start_time = time.time()  # Start time for reference
        print(f'[MOTOR{motor_id} SLEEP STARTED] Seconds: {seconds}')
        time.sleep(seconds) 
        print(f'[MOTOR{motor_id} SLEEP FINISHED] Real break time: {time.time() - start_time:.2f}')

    def run_using_velocities_array(self, velocities, target_angles, motor_id=''):
        print(f'[MOTOR{motor_id} MOVEMENT STARTED] Movement in progress...')
        start_time = time.time()

        # Initialize PID variables
        integral = 0
        previous_error = 0

        times = []
        angles = []

        for velocity, target_angle in zip(velocities, target_angles):
            try:
                if velocity > 0:
                    direction = 'plus'
                else:
                    direction = 'minus'

                speed_percentage = max(0, min(100, abs(velocity)))

                # Run the motor at the start to set initial movement
                self.motor.run_motor(direction, speed_percentage)

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

                # Record time and angle
                times.append(current_time)
                angles.append(current_angle)

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
        print(f"[MOTOR{motor_id} FINISHED MOVEMENT] Total runtime: {time.time() - start_time:.2f} seconds")
        # Plotting the motor angle over time
        plt.figure(figsize=(10, 5))
        plt.plot(times, angles, label='Motor Angle', marker='o')
        plt.title(f'Motor{motor_id} Angle Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Motor Angle (degrees)')
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{get_filename_datetime()}_motor{motor_id}.png")
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