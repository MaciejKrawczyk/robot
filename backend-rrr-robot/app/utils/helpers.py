import datetime
import numpy as np
import math


def degrees_to_radians(degrees: float):
    radians = degrees * (math.pi / 180)
    return radians


def radians_to_degrees(radians: float):
    degrees = radians * (180 / np.pi)
    return degrees


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


def get_filename_datetime():
    now = datetime.datetime.now()
    formatted = now.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted


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