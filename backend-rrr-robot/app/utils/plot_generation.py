import matplotlib.pyplot as plt
import numpy as np
from .kinematics import inverse_kinematics3
from types_global import PointXYZ


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
    from collections import defaultdict

    plot_directory = 'motor_plots'
    os.makedirs(plot_directory, exist_ok=True)

    # Group files by date and time
    files_by_datetime = defaultdict(list)
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            # Extract date and time from filename
            date_time = '_'.join(filename.split('_')[:2])
            files_by_datetime[date_time].append(filename)

    # Plot files grouped by date and time
    for date_time, filenames in files_by_datetime.items():
        num_files = len(filenames)
        fig_angle, axs_angle = plt.subplots(num_files, 1, figsize=(10, 5 * num_files), squeeze=False)
        fig_error, axs_error = plt.subplots(num_files, 1, figsize=(10, 5 * num_files), squeeze=False)

        for i, filename in enumerate(filenames):
            filepath = os.path.join(directory, filename)
            times, actual_angles, target_angles, pid_outputs, errors = [], [], [], [], []
            with open(filepath, 'r') as file:
                for line in file:
                    time_point, actual_angle, target_angle, pid_output, error = line.strip().split(',')
                    times.append(float(time_point))
                    actual_angles.append(float(actual_angle))
                    target_angles.append(float(target_angle))
                    pid_outputs.append(float(pid_output))
                    errors.append(float(error))

            # Plotting the motor angle data
            axs_angle[i, 0].plot(times, actual_angles, 'o-', label='Actual Motor Angle')
            axs_angle[i, 0].plot(times, target_angles, 'x--', label='Target Motor Angle')
            motor_id = filename.split('_')[2]  # Adjusted to get motor_id correctly
            axs_angle[i, 0].set_title(f'Motor {motor_id} Angle Over Time')
            axs_angle[i, 0].set_xlabel('Time (seconds)')
            axs_angle[i, 0].set_ylabel('Motor Angle (degrees)')
            axs_angle[i, 0].grid(True)
            axs_angle[i, 0].legend()

            # Plotting the error data
            axs_error[i, 0].plot(times, errors, 's-', color='red', label='Error')
            axs_error[i, 0].set_title(f'Motor {motor_id} Error Over Time')
            axs_error[i, 0].set_xlabel('Time (seconds)')
            axs_error[i, 0].set_ylabel('Error')
            axs_error[i, 0].grid(True)
            axs_error[i, 0].legend()

        plt.tight_layout()
        plot_filename_angle = os.path.join(plot_directory, f"{date_time}_all_motors_angle_plot.png")
        plot_filename_error = os.path.join(plot_directory, f"{date_time}_all_motors_error_plot.png")
        fig_angle.savefig(plot_filename_angle)
        fig_error.savefig(plot_filename_error)
        plt.close(fig_angle)
        plt.close(fig_error)
        
        
        
# def read_coordinates(file_path):
#     with open(file_path, 'r') as file:
#         coordinates = file.readline().strip().split(',')
#         coordinates = [float(coord) for coord in coordinates]
#     return coordinates

# def plot_3d_curve(x_file, y_file, z_file):
#     x = read_coordinates(x_file)
#     y = read_coordinates(y_file)
#     z = read_coordinates(z_file)

#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     ax.plot(x, y, z, label='3D Curve')
#     ax.set_xlabel('X Coordinate')
#     ax.set_ylabel('Y Coordinate')
#     ax.set_zlabel('Z Coordinate')
#     ax.legend()

#     plt.savefig('figdif')
#     plt.show()

# # Example usage
# plot_3d_curve(
#     'motor_data/2024-05-17_15-45-35_motor1_data.txt', 
#     'motor_data/2024-05-17_15-45-35_motor2_data.txt', 
#     'motor_data/2024-05-17_15-45-35_motor3_data.txt'
#     )


# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


def plot_bezier_curve_and_control_points(trajectory, control_points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the Bézier curve
    xs = [point.x for point in trajectory]
    ys = [point.y for point in trajectory]
    zs = [point.z for point in trajectory]
    ax.scatter(xs, ys, zs, label='Bézier Curve', c='blue')

    # Plot control points
    cp_xs = [control_points.A.x, control_points.B.x, control_points.C.x, control_points.D.x]
    cp_ys = [control_points.A.y, control_points.B.y, control_points.C.y, control_points.D.y]
    cp_zs = [control_points.A.z, control_points.B.z, control_points.C.z, control_points.D.z]

    ax.scatter(cp_xs, cp_ys, cp_zs, color='red')
    for i, txt in enumerate(['A', 'B', 'C', 'D']):
        ax.text(cp_xs[i], cp_ys[i], cp_zs[i], txt, color='red')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Bézier Curve and Control Points')
    ax.legend()
    plt.show()


def plot_combined_curve_and_workspace(trajectory, control_points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the Bézier curve
    xs = [point.x for point in trajectory]
    ys = [point.y for point in trajectory]
    zs = [point.z for point in trajectory]
    ax.scatter(xs, ys, zs, label='Bézier Curve', c='blue')

    # Plot control points
    cp_xs = [control_points.A.x, control_points.B.x, control_points.C.x, control_points.D.x]
    cp_ys = [control_points.A.y, control_points.B.y, control_points.C.y, control_points.D.y]
    cp_zs = [control_points.A.z, control_points.B.z, control_points.C.z, control_points.D.z]

    ax.scatter(cp_xs, cp_ys, cp_zs, color='red')
    for i, txt in enumerate(['A', 'B', 'C', 'D']):
        ax.text(cp_xs[i], cp_ys[i], cp_zs[i], txt, color='red')

    # Generate workspace points
    num_samples_theta1 = 50
    num_samples_theta2 = 20
    num_samples_theta3 = 20
    theta1_vals = np.linspace(*joint_limits[0], num_samples_theta1)
    theta2_vals = np.linspace(*joint_limits[1], num_samples_theta2)
    theta3_vals = np.linspace(*joint_limits[2], num_samples_theta3)

    x, y, z = [], [], []

    # Calculate positions for all combinations of joint angles
    for i, theta1 in enumerate(theta1_vals):
        if i % 2 == 0:  # Take every second value of theta1
            for theta2 in theta2_vals:
                for theta3 in theta3_vals:
                    pos = forward_kinematics(theta1, theta2, theta3)
                    x.append(pos[0])
                    y.append(pos[1])
                    z.append(pos[2])

    # Plot the workspace points
    ax.scatter(x, y, z, c='r', marker='o', s=0.1, label='Workspace')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Workspace of the RRR Manipulator with Bézier Curve')
    ax.legend()
    plt.show()


def plot_theta_changes(trajectory):
    thetas = [inverse_kinematics3(point.x, point.y, point.z) for point in trajectory]

    for theta in thetas:
        print(theta)

    theta1_vals = [theta.theta1 for theta in thetas]
    theta2_vals = [theta.theta2 for theta in thetas]
    theta3_vals = [theta.theta3 for theta in thetas]

    t_vals = np.arange(0, 1.01, 0.01)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

    ax1.plot(t_vals, theta1_vals, label='Theta 1')
    ax1.set_xlabel('t')
    ax1.set_ylabel('Theta 1')
    ax1.legend()

    ax2.plot(t_vals, theta2_vals, label='Theta 2')
    ax2.set_xlabel('t')
    ax2.set_ylabel('Theta 2')
    ax2.legend()

    ax3.plot(t_vals, theta3_vals, label='Theta 3')
    ax3.set_xlabel('t')
    ax3.set_ylabel('Theta 3')
    ax3.legend()

    plt.show()


def plot_XYZ_changes(trajectory):
    thetas = [PointXYZ(point.x, point.y, point.z) for point in trajectory]

    # for theta in thetas:
    #     print(theta)
    #
    theta1_vals = [theta.x for theta in thetas]
    theta2_vals = [theta.y for theta in thetas]
    theta3_vals = [theta.z for theta in thetas]

    t_vals = np.arange(0, 1.01, 0.01)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

    ax1.plot(t_vals, theta1_vals, label='X')
    ax1.set_xlabel('t')
    ax1.set_ylabel('X')
    ax1.legend()

    ax2.plot(t_vals, theta2_vals, label='Y')
    ax2.set_xlabel('t')
    ax2.set_ylabel('Y')
    ax2.legend()

    ax3.plot(t_vals, theta3_vals, label='Z')
    ax3.set_xlabel('t')
    ax3.set_ylabel('Z')
    ax3.legend()

    plt.show()
    
    
def plot_motor_data_msq(filename):
    # import matplotlib.pyplot as plt

    times = []
    actual_angles = []
    target_angles = []
    pid_outputs = []
    errors = []

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            # if line.startswith("Mean Square Error"):
            #     mse = float(line.split(":")[1].strip())
            #     continue
            time_point, actual_angle, target_angle, pid_output, error = map(float, line.split(','))
            times.append(time_point)
            actual_angles.append(actual_angle)
            target_angles.append(target_angle)
            pid_outputs.append(pid_output)
            errors.append(error)
    
    plt.figure(figsize=(10, 8))
    
    plt.subplot(3, 1, 1)
    plt.plot(times, actual_angles, label='Actual Angle')
    plt.plot(times, target_angles, label='Target Angle')
    plt.title('Motor Angles')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (degrees)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(times, pid_outputs, label='PID Output', color='red')
    plt.title('PID Output')
    plt.xlabel('Time (s)')
    plt.ylabel('PID Output')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.plot(times, errors, label='Error', color='green')
    plt.title('Error Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Error (degrees)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    plt.savefig('fsdsdfsdfsfd')
    
    plt.show()