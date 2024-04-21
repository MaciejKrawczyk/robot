from MotorEncoderCombo import MotorEncoderCombo
import time
# import matplotlib.pyplot as plt

PULSES_PER_REVOLUTION = 1250


class MotorController:
    def __init__(self, motor: MotorEncoderCombo):
        self.motor = motor

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