import datetime
import numpy as np
import math


def transform_to_numpy(points):
    x_coords = [round(point['x'], 2) for point in points]
    y_coords = [round(point['y'], 2) for point in points]
    z_coords = [round(point['z'], 2) for point in points]
    numpy_array = np.array([x_coords, y_coords, z_coords])
    return numpy_array


def percent_to_value(percent):
    """
    Convert a percentage to a value between 0 and 65535.
    Args: percent (float): The percentage (0.0 - 100.0).
    Returns: int: The corresponding value in the range 0 to 65535.
    """
    if percent < 0:
        percent = 0
    elif percent > 100:
        percent = 100

    value = int((percent / 100) * 65535)
    return value


def decimal_to_hex(decimal_number):
    if isinstance(decimal_number, int):
        return hex(decimal_number)
    else:
        raise ValueError("Input must be an integer.")


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
    vx = np.gradient(x, step_size)
    vy = np.gradient(y, step_size)
    vz = np.gradient(z, step_size)
    
    return vx, vy, vz