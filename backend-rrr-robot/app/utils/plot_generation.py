import matplotlib.pyplot as plt
import numpy as np


def plot_positions(x, y, z, total_time, file_name='position_over_time'):
    t = np.linspace(0, total_time, len(x))  # actual time in seconds
    plt.figure(figsize=(10, 6))
    plt.plot(t, x, label='X position', color='green')
    plt.plot(t, y, label='Y position', color='blue')
    plt.plot(t, z, label='Z position', color='black')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Position')
    plt.title('Position Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{file_name}.png") 
    plt.show()


def plot_angles(theta1, theta2, theta3, total_time, file_name='angles_over_time'):
    t = np.linspace(0, total_time, len(theta1))
    plt.figure(figsize=(10, 6))
    plt.plot(t, theta1, label='Theta1 angle', color='green')
    plt.plot(t, theta2, label='Theta2 angle', color='blue')
    plt.plot(t, theta3, label='Theta3 angle', color='black')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Angles')
    plt.title('Angles Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{file_name}.png")
    plt.show()


# def plot_velocity(x, y, z, step_size, file_name='velocity_over_time'):
#     # Calculate velocities using the separated function
#     vx, vy, vz = calculate_velocity(x, y, z, step_size)
    
#     # Determine the maximum velocity to scale to percentage
#     # max_velocity = max(np.max(np.abs(vx)), np.max(np.abs(vy)), np.max(np.abs(vz)))
    
#     # Normalize velocities to a percentage of the maximum velocity
#     # vx_percent = (vx / max_velocity) * 100
#     # vy_percent = (vy / max_velocity) * 100
#     # vz_percent = (vz / max_velocity) * 100
    
#     vx_percent = vx
#     vy_percent = vy
#     vz_percent = vz
    
#     # Plot the velocities
#     t = np.linspace(0, len(x) * step_size, len(vx))  # actual time in seconds
#     plt.figure(figsize=(10, 6))
#     plt.plot(t, vx_percent, label='X Velocity (%)', color='red')
#     plt.plot(t, vy_percent, label='Y Velocity (%)', color='blue')
#     plt.plot(t, vz_percent, label='Z Velocity (%)', color='black')
#     plt.xlabel('Time (seconds)')
#     plt.ylabel('Velocity (%)')
#     plt.title('Velocity Over Time (Percentage)')
#     plt.legend()
#     plt.grid(True)  # Enable grid lines
#     plt.savefig(f"{file_name}.png")  # Save the plot as a PNG file
#     plt.show()
    
    
def plot_velocity_with_calculated_velocitites(x, vx, vy, vz, step_size, file_name='velocity_over_time'):
    # Determine the maximum velocity to scale to percentage
    max_velocity = max(np.max(np.abs(vx)), np.max(np.abs(vy)), np.max(np.abs(vz)))
    
    # Normalize velocities to a percentage of the maximum velocity
    vx_percent = (vx / max_velocity) * 100
    vy_percent = (vy / max_velocity) * 100
    vz_percent = (vz / max_velocity) * 100
    
    # vx_percent = vx
    
    # Plot the velocities
    t = np.linspace(0, len(x) * step_size, len(vx))  # actual time in seconds
    plt.figure(figsize=(10, 6))
    plt.plot(t, vx_percent, label='X Velocity (%)', color='red')
    plt.plot(t, vy_percent, label='Y Velocity (%)', color='blue')
    plt.plot(t, vz_percent, label='Z Velocity (%)', color='black')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity (%)')
    plt.title('Velocity Over Time (Percentage)')
    plt.legend()
    plt.grid(True)  # Enable grid lines
    plt.savefig(f"{file_name}.png")  # Save the plot as a PNG file
    plt.show()
    
    
def plot_angle_velocity(vtheta1, vtheta2, vtheta3, step_size, file_name='velocity_over_time'):
    # Determine the maximum velocity to scale to percentage
    max_velocity = max(np.max(np.abs(vtheta1)), np.max(np.abs(vtheta2)), np.max(np.abs(vtheta3)))
    
    # Normalize velocities to a percentage of the maximum velocity
    vx_percent = (vtheta1 / max_velocity) * 100
    vy_percent = (vtheta2 / max_velocity) * 100
    vz_percent = (vtheta3 / max_velocity) * 100
    
    t = np.linspace(0, len(vtheta1) * step_size, len(vtheta1))  # actual time in seconds
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, vx_percent, label='Theta1 Velocity (%)', color='green')
    plt.plot(t, vy_percent, label='Theta2 Velocity (%)', color='blue')
    plt.plot(t, vz_percent, label='Theta3 Velocity (%)', color='black')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity (%)')
    plt.title('Velocity Over Time (Percentage)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{file_name}.png")
    plt.show()
    
    
def plot_position_velocity(vx, vy, vz, step_size, file_name='velocity_over_time'):
    # Determine the maximum velocity to scale to percentage
    max_velocity = max(np.max(np.abs(vx)), np.max(np.abs(vy)), np.max(np.abs(vz)))
    
    # Normalize velocities to a percentage of the maximum velocity
    vx_percent = (vx / max_velocity) * 100
    vy_percent = (vy / max_velocity) * 100
    vz_percent = (vz / max_velocity) * 100
    
    # vx_percent = vx
    
    # Plot the velocities
    t = np.linspace(0, len(vx) * step_size, len(vx))  # actual time in seconds
    plt.figure(figsize=(10, 6))
    plt.plot(t, vx_percent, label='X Velocity (%)', color='green')
    plt.plot(t, vy_percent, label='Y Velocity (%)', color='blue')
    plt.plot(t, vz_percent, label='Z Velocity (%)', color='black')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity (%)')
    plt.title('Velocity Over Time (Percentage)')
    plt.legend()
    plt.grid(True)  # Enable grid lines
    plt.savefig(f"{file_name}.png")  # Save the plot as a PNG file
    plt.show()
    
    
    
def plot_all_motor_data(directory='motor_data'):
    import matplotlib.pyplot as plt
    import os

    # Ensure output directory for plots exists
    plot_directory = 'motor_plots'
    os.makedirs(plot_directory, exist_ok=True)

    # List all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            times, actual_angles, target_angles, pid_outputs = [], [], [], []
            with open(filepath, 'r') as file:
                for line in file:
                    time_point, actual_angle, target_angle, pid_output = line.strip().split(',')
                    times.append(float(time_point))
                    actual_angles.append(float(actual_angle))
                    target_angles.append(float(target_angle))
                    pid_outputs.append(float(pid_output))

            # Plotting the data
            plt.figure(figsize=(10, 5))
            plt.plot(times, actual_angles, 'o-', label='Actual Motor Angle')
            plt.plot(times, target_angles, 'x--', label='Target Motor Angle')
            filename_split = filename.split('_')
            motor_id = filename_split[2]
            date = filename_split[0]
            time = filename_split[1]
            plt.title(f'Motor{motor_id} Angle Over Time')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Motor Angle (degrees)')
            plt.grid(True)
            plt.legend()
            plot_filename = os.path.join(plot_directory, f"{date}_{time}_{motor_id}_plot.png")
            plt.savefig(plot_filename)
            plt.close()