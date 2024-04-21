import matplotlib.pyplot as plt
import numpy as np


def plot_positions(x, y, z, total_time, file_name='position_over_time'):
    t = np.linspace(0, total_time, len(x))  # actual time in seconds
    plt.figure(figsize=(10, 6))
    plt.plot(t, x, label='X position', color='red')
    plt.plot(t, y, label='Y position', color='blue')
    plt.plot(t, z, label='Z position', color='black')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Position')
    plt.title('Position Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{file_name}.png") 
    plt.show()


def plot_angles(theta1, theta2, theta3, total_time, file_name='position_over_time'):
    t = np.linspace(0, total_time, len(theta1))
    plt.figure(figsize=(10, 6))
    plt.plot(t, theta1, label='Theta1 angle', color='red')
    plt.plot(t, theta2, label='Theta2 angle', color='blue')
    plt.plot(t, theta3, label='Theta3 angle', color='black')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Position')
    plt.title('Position Over Time')
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