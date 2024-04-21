import math
from typing import List

import numpy as np
import matplotlib.pyplot as plt

import datetime
from kinematics_utils import inverse_kinematics3


# class BezierVector3D:
#     def __init__(self, x, y, z) -> None:
#         self.x = x
#         self.y = y
#         self.z = z
        
#     def __str__(self):  
#         return f"({self.x}, {self.y}, {self.z})"



import numpy as np

def radians_to_degrees(radians):
    return radians * 180 / np.pi

def add_points(points, calm):
    x1 = points[0, :]
    y1 = points[1, :]
    z1 = points[2, :]
    
    distx = x1[1] - x1[0]
    disty = y1[1] - y1[0]
    distz = z1[1] - z1[0]
    
    x = np.zeros(points.shape[1] * 3)
    y = np.zeros(points.shape[1] * 3)
    z = np.zeros(points.shape[1] * 3)
    
    for i in range(points.shape[1]):
        x[i*3] = x1[i]
        y[i*3] = y1[i]
        z[i*3] = z1[i]

    TH, R, Z = cart2pol(distx, disty, distz)
    TH += calm * np.pi / 4
    R *= 0.4 * calm
    Z *= 0.4 * calm
    a, b, c = pol2cart(TH, R, Z)
    
    x[1] = a + x1[0]
    y[1] = b + y1[0]
    z[1] = c + z1[0]
    
    # Calculate for the last point
    distx = x1[-1] - x1[-2]
    disty = y1[-1] - y1[-2]
    distz = z1[-1] - z1[-2]
    
    TH, R, Z = cart2pol(distx, disty, distz)
    TH -= calm * np.pi / 4
    R *= 0.4 * calm
    Z *= 0.4 * calm
    a, b, c = pol2cart(TH, R, Z)
    
    x[-2] = x1[-1] - a
    y[-2] = y1[-1] - b
    z[-2] = z1[-1] - c
    
    # Calculate for intermediate points
    for i in range(1, points.shape[1] - 1):
        distx = (x1[i + 1] - x1[i - 1]) / 2
        disty = (y1[i + 1] - y1[i - 1]) / 2
        distz = (z1[i + 1] - z1[i - 1]) / 2
        TH, R, Z = cart2pol(distx, disty, distz)
        TH *= (-1)**(i+1) * calm * np.pi / 2
        R *= 0.3 * calm
        Z *= 0.3 * calm
        a, b, c = pol2cart(TH, R, Z)
        
        x[3*i-2] = x1[i] - a
        y[3*i-2] = y1[i] - b
        z[3*i-2] = z1[i] - c
        
        x[3*i] = x1[i] + a
        y[3*i] = y1[i] + b
        z[3*i] = z1[i] + c
        
    return x, y, z


def cart2pol(x, y, z):
    R = np.sqrt(x**2 + y**2 + z**2)
    TH = np.arctan2(np.sqrt(x**2 + y**2), z)
    Z = np.arctan2(y, x)
    return TH, R, Z


def pol2cart(TH, R, Z):
    x = R * np.sin(TH) * np.cos(Z)
    y = R * np.sin(TH) * np.sin(Z)
    z = R * np.cos(TH)
    return x, y, z


# def bezier(X, Y, Z, speed):
#     x, y, z = np.array([]), np.array([]), np.array([])
    
#     # Process each segment of four points
#     for i in range(0, len(X)-1, 3):
#         if i + 3 >= len(X):
#             break
#         p0 = np.array([X[i], Y[i], Z[i]])
#         p1 = np.array([X[i+1], Y[i+1], Z[i+1]])
#         p2 = np.array([X[i+2], Y[i+2], Z[i+2]])
#         p3 = np.array([X[i+3], Y[i+3], Z[i+3]])
        
#         t = np.linspace(0, 1, int(1/speed) + 1)
#         curve_x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
#         curve_y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
#         curve_z = (1 - t)**3 * p0[2] + 3 * (1 - t)**2 * t * p1[2] + 3 * (1 - t) * t**2 * p2[2] + t**3 * p3[2]
        
#         x = np.concatenate([x, curve_x])
#         y = np.concatenate([y, curve_y])
#         z = np.concatenate([z, curve_z])
    
#     return x, y, z


def inverse_kinematics_numpy(x, y, z, l1=1, l2=1, l3=1):
    h = l1
    L1 = l2
    L2 = l3

    theta1 = np.arctan2(y, x)
    r2 = z - h
    r1 = np.sqrt(x ** 2 + y ** 2)
    r3 = np.sqrt(r1 ** 2 + r2 ** 2)
    fi1 = np.arctan2(r2, r1)
    fi2 = np.arccos(np.clip((L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3), -1.0, 1.0))
    theta2 = fi2 + fi1
    fi3 = np.arccos(np.clip((r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2), -1.0, 1.0))
    theta3 = fi3 - np.pi

    angles = (
        radians_to_degrees(theta1),
        radians_to_degrees(theta2),
        radians_to_degrees(theta3)
    )
    return angles


def bezier(X, Y, Z, speed):
    x, y, z = np.array([]), np.array([]), np.array([])
    
    # Process each segment of four points
    for i in range(0, len(X) - 1, 3):
        if i + 3 >= len(X):
            break
        p0 = np.array([X[i], Y[i], Z[i]])
        p1 = np.array([X[i+1], Y[i+1], Z[i+1]])
        p2 = np.array([X[i+2], Y[i+2], Z[i+2]])
        p3 = np.array([X[i+3], Y[i+3], Z[i+3]])
        
        t = np.linspace(0, 1, int(1/speed) + 1)
        curve_x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
        curve_y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
        curve_z = (1 - t)**3 * p0[2] + 3 * (1 - t)**2 * t * p1[2] + 3 * (1 - t) * t**2 * p2[2] + t**3 * p3[2]
        
        x = np.concatenate([x, curve_x])
        y = np.concatenate([y, curve_y])
        z = np.concatenate([z, curve_z])
    
    # Calculate angles after generating the full curve
    # Assume that inverse_kinematics_numpy returns a tuple (theta1, theta2, theta3)
    angles = np.array([inverse_kinematics_numpy(x[i], y[i], z[i]) for i in range(len(x))])
    theta1 = angles[:, 0]
    theta2 = angles[:, 1]
    theta3 = angles[:, 2]
    
    return x, y, z, theta1, theta2, theta3


def modify_curve(bezier_result_x, bezier_result_y, bezier_result_z, modify_func):
    x = bezier_result_x
    y = bezier_result_y
    z = bezier_result_z
    print('before modyfing curve', x)

    modified_x, modified_y, modified_z = np.array([]), np.array([]), np.array([])
    
    for i in range(len(x)):
        # mx, my, mz = modify_func(x[i], y[i], z[i], 1, 1, 1)
        position = modify_func(x[i], y[i], z[i], 1, 1, 1)
        modified_x = np.append(modified_x, position['theta1'])
        modified_y = np.append(modified_y, position['theta2'])
        modified_z = np.append(modified_z, position['theta3'])
    
    return modified_x, modified_y, modified_z



def calculate_velocity(x, y, z, step_size):
    # print(x)
    # print(y)
    # Calculate velocity components for each dimension
    vx = np.gradient(x, step_size)
    vy = np.gradient(y, step_size)
    vz = np.gradient(z, step_size)
    
    # max_velocity = max(np.max(np.abs(vx)), np.max(np.abs(vy)), np.max(np.abs(vz)))
    # vx_percent = (vx / max_velocity) * 100
    # vy_percent = (vy / max_velocity) * 100
    # vz_percent = (vz / max_velocity) * 100
    
    return vx, vy, vz
    # return vx_percent, vy_percent, vz_percent


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
    plt.grid(True)  # Enable grid lines
    plt.savefig(f"{file_name}.png")  # Save the plot as a PNG file
    plt.show()


def plot_angles(theta1, theta2, theta3, total_time, file_name='position_over_time'):
    t = np.linspace(0, total_time, len(theta1))  # actual time in seconds
    plt.figure(figsize=(10, 6))
    plt.plot(t, theta1, label='Theta1 angle', color='red')
    plt.plot(t, theta2, label='Theta2 angle', color='blue')
    plt.plot(t, theta3, label='Theta3 angle', color='black')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Position')
    plt.title('Position Over Time')
    plt.legend()
    plt.grid(True)  # Enable grid lines
    plt.savefig(f"{file_name}.png")  # Save the plot as a PNG file
    plt.show()


def plot_velocity(x, y, z, step_size, file_name='velocity_over_time'):
    # Calculate velocities using the separated function
    vx, vy, vz = calculate_velocity(x, y, z, step_size)
    
    # Determine the maximum velocity to scale to percentage
    # max_velocity = max(np.max(np.abs(vx)), np.max(np.abs(vy)), np.max(np.abs(vz)))
    
    # Normalize velocities to a percentage of the maximum velocity
    # vx_percent = (vx / max_velocity) * 100
    # vy_percent = (vy / max_velocity) * 100
    # vz_percent = (vz / max_velocity) * 100
    
    vx_percent = vx
    vy_percent = vy
    vz_percent = vz
    
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


def get_filename_datetime():
    # Current date and time
    now = datetime.datetime.now()
    # Format as a string suitable for filenames
    formatted = now.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted


def shortest_path(X, Y, Z, speed):
    # Calculate the number of points to interpolate based on the speed parameter
    x, y, z = [], [], []
    segments = len(X) - 1
    
    for i in range(segments):
        p0 = np.array([X[i], Y[i], Z[i]])
        p1 = np.array([X[i+1], Y[i+1], Z[i+1]])
        
        # Determine the number of interpolation points based on the distance between points and speed
        dist = np.linalg.norm(p1 - p0)
        steps = max(int(dist / speed), 1)  # ensure at least one point
        
        t = np.linspace(0, 1, steps + 1)  # +1 to include the endpoint
        line_x = (1 - t) * p0[0] + t * p1[0]
        line_y = (1 - t) * p0[1] + t * p1[1]
        line_z = (1 - t) * p0[2] + t * p1[2]
        
        # Append points to the list
        x.extend(line_x)
        y.extend(line_y)
        z.extend(line_z)
    
    # Convert lists to numpy arrays for consistency with the bezier output
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    
    # Calculate angles if required by following the kinematics model you might have
    angles = np.array([inverse_kinematics_numpy(x[i], y[i], z[i]) for i in range(len(x))])
    theta1 = angles[:, 0]
    theta2 = angles[:, 1]
    theta3 = angles[:, 2]
    
    return x, y, z, theta1, theta2, theta3


# step_size = 0.01
# calm = 0.5

# points_array = np.array([
#     [2, -2, 0.12, -1.95],  # x-coordinates
#     [0, 0.01, -0.11, 0.17],    # y-coordinates
#     [1, 1.01, 1.55, 1.29]   # z-coordinates
# ])

# X, Y, Z = add_points(points_array, calm)

# x, y, z = bezier(X, Y, Z, 0.01)

# total_time = len(x) * step_size 
# plot_positions(x, y, z, total_time)
# plot_velocity(x, y, z, step_size)

