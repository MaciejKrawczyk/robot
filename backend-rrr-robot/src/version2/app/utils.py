import math
from typing import List

import numpy as np
import matplotlib.pyplot as plt


# class BezierVector3D:
#     def __init__(self, x, y, z) -> None:
#         self.x = x
#         self.y = y
#         self.z = z
        
#     def __str__(self):  
#         return f"({self.x}, {self.y}, {self.z})"



import numpy as np

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



def bezier(X, Y, Z, speed):
    x, y, z = np.array([]), np.array([]), np.array([])
    
    # Process each segment of four points
    for i in range(0, len(X)-1, 3):
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
    
    return x, y, z


# The points you provided are in a non-Numpy format, so let's convert them.
points_array = np.array([
    [1, 2.5, 4],  # x-coordinates
    [1, 3, 4],    # y-coordinates
    [1, 1.5, 4]   # z-coordinates
])

# Add points for Bezier curve
calm = 0.5
X, Y, Z = add_points(points_array, calm)

# Calculate the Bezier curve with a small speed (for high resolution)
x, y, z = bezier(X, Y, Z, 0.01)

step_size = 0.01

def plot_positions(x, y, z, total_time):
    t = np.linspace(0, total_time, len(x))  # actual time in seconds
    plt.figure(figsize=(10, 6))
    plt.plot(t, x, label='X position')
    plt.plot(t, y, label='Y position')
    plt.plot(t, z, label='Z position')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Position')
    plt.title('Position Over Time')
    plt.legend()
    plt.savefig("position_over_time.png")  # Save the plot as a PNG file
    plt.show()

def plot_velocity(x, y, z, step_size):
    vx = np.gradient(x, step_size)
    vy = np.gradient(y, step_size)
    vz = np.gradient(z, step_size)
    
    t = np.linspace(0, len(x) * step_size, len(vx))  # actual time in seconds
    plt.figure(figsize=(10, 6))
    plt.plot(t, vx, label='X Velocity')
    plt.plot(t, vy, label='Y Velocity')
    plt.plot(t, vz, label='Z Velocity')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity')
    plt.title('Velocity Over Time')
    plt.legend()
    plt.savefig("velocity_over_time.png")  # Save the plot as a PNG file
    plt.show()

# Using the functions to visualize position and velocity
total_time = len(x) * step_size  # Total time span based on number of points and step size
plot_positions(x, y, z, total_time)
plot_velocity(x, y, z, step_size)

