import numpy as np
from .helpers import pol2cart, cart2pol, radians_to_degrees
import math
from .kinematics import forward_kinematics
from modules.bezier.Bezier import Bezier
from config import Config

def cart2pol(x, y, z):
    rho = np.sqrt(x**2 + y**2 + z**2)
    phi = np.arctan2(y, x)
    theta = np.arccos(z / rho)
    return phi, rho, theta

def pol2cart(phi, rho, theta):
    x = rho * np.sin(theta) * np.cos(phi)
    y = rho * np.sin(theta) * np.sin(phi)
    z = rho * np.cos(theta)
    return x, y, z

def add_points(points, calm):
    """
    aby dodać omijanie przeszkód, należy zmodyfikować tę funckję
    """
    # Extract x, y, z from points array
    x1, y1, z1 = points[0, :], points[1, :], points[2, :]
    
    # Initialize the output lists
    x, y, z = [], [], []

    # Calculate control points for the start point
    distx, disty, distz = x1[1] - x1[0], y1[1] - y1[0], z1[1] - z1[0]
    th, r, zz = cart2pol(distx, disty, distz)
    th += calm * np.pi / 4
    r *= 0.4 * calm
    zz *= 0.4 * calm
    a, b, c = pol2cart(th, r, zz)

    # Append start point control
    x.append(x1[0])
    y.append(y1[0])
    z.append(z1[0])
    x.append(a + x1[0])
    y.append(b + y1[0])
    z.append(c + z1[0])

    # Loop through middle points
    for i in range(1, len(x1)-1):
        distx = (x1[i+1] - x1[i-1]) / 2
        disty = (y1[i+1] - y1[i-1]) / 2
        distz = (z1[i+1] - z1[i-1]) / 2
        th, r, zz = cart2pol(distx, disty, distz)
        th *= (-1)**(i+1) * calm * np.pi / 2
        r *= 0.3 * calm
        zz *= 0.3 * calm
        a, b, c = pol2cart(th, r, zz)

        # Append control points for middle points
        x.append(x1[i] - a)
        y.append(y1[i] - b)
        z.append(z1[i] - c)
        x.append(x1[i])
        y.append(y1[i])
        z.append(z1[i])
        x.append(x1[i] + a)
        y.append(y1[i] + b)
        z.append(z1[i] + c)

    # Calculate and append control points for the end point
    distx, disty, distz = x1[-1] - x1[-2], y1[-1] - y1[-2], z1[-1] - z1[-2]
    th, r, zz = cart2pol(distx, disty, distz)
    th -= calm * np.pi / 4
    r *= 0.4 * calm
    zz *= 0.4 * calm
    a, b, c = pol2cart(th, r, zz)

    x.append(x1[-1] - a)
    y.append(y1[-1] - b)
    z.append(z1[-1] - c)
    x.append(x1[-1])
    y.append(y1[-1])
    z.append(z1[-1])

    return x, y, z


def wrap_angle(angle):
    return (angle + np.pi) % (2 * np.pi)


def check_if_point_in_degrees_in_workspace(theta1, theta2, theta3):
    theta1_lengths = (0, 360)
    theta2_lengths = (-45, 90)
    theta3_lengths = (-135, 0)
    
    if theta1 > theta1_lengths[0] and theta1 < theta1_lengths[1]:
        if theta2 > theta2_lengths[0] and theta2 < theta2_lengths[1]:
            if theta3 > theta3_lengths[0] and theta3 < theta3_lengths[1]:
                return True
    else:
        return False


def inverse_kinematics_numpy(x, y, z, l1=14, l2=9, l3=9):
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


def inverse_kinematics_numpy_2( x, y, z, l1=14, l2=9, l3=9):
    """
    wg filmiku z yt https://www.youtube.com/watch?v=D93iQVoSScQ
    elbow up
    """

    h = l1
    L1 = l2
    L2 = l3

    theta1 = math.atan2(y, x)  # 1
    r2 = z - h  # 4
    r1 = math.sqrt(x ** 2 + y ** 2)  #
    r3 = math.sqrt(r1 ** 2 + r2 ** 2)  #
    fi2 = math.atan2(r2, r1)  # 3
    fi1 = np.arccos(np.clip((L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3), -1.0, 1.0))
    theta2 = fi2 - fi1
    fi3 = np.arccos(np.clip((r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2), -1.0, 1.0))
    theta3 = math.pi - fi3  #

    angles = (
        radians_to_degrees(theta1),
        radians_to_degrees(theta2),
        radians_to_degrees(theta3)
    )
    return angles


def check_if_positive(number: float):
    if number > 0:
        return True
    else:
        return False
    
def check_if_negative(number: float):
    if number < 0:
        return True
    else:
        return False

def has_zero_between(a, b):
    return a * b < 0

def check_quarters_of_x(list_of_x_values, list_of_y_values, list_of_z_values):
    
    is_quarter_from_I_II = False
    is_quarter_from_II_to_III = False
    is_quarter_from_III_to_IV = False
    is_quarter_from_II_to_I = False
    is_quarter_from_III_to_II = False
    is_quarter_from_IV_to_III = False
    
    has_x_went_from_minus_to_plus = False
    has_x_went_from_plus_to_minus = False
    
    angles = np.array([inverse_kinematics_numpy(list_of_x_values[i], list_of_y_values[i], list_of_z_values[i]) for i in range(len(list_of_x_values))])
    list_of_theta1 = angles[:, 0]
    list_of_theta2 = angles[:, 1]
    list_of_theta3 = angles[:, 2]
    
    for i in range(1, len(list_of_x_values)):            
        current_x = list_of_x_values[i]
        previous_x = list_of_x_values[i-1]
        
        current_y = list_of_y_values[i]
        previous_y = list_of_y_values[i-1]
        
        current_z = list_of_z_values[i]
        previous_z = list_of_z_values[i-1]
        
        # check if change quarter from II to III
        if check_if_negative(current_x) and check_if_negative(previous_x) and check_if_positive(previous_y) and check_if_negative(current_y):
            is_quarter_from_I_II = False
            is_quarter_from_II_to_III = True
            is_quarter_from_III_to_IV = False
            is_quarter_from_II_to_I = False
            is_quarter_from_III_to_II = False
            is_quarter_from_IV_to_III = False
        
        # check if change quarter from III to II
        if check_if_negative(current_x) and check_if_negative(previous_x) and check_if_negative(previous_y) and check_if_positive(current_y):       
            is_quarter_from_I_II = False
            is_quarter_from_II_to_III = False
            is_quarter_from_III_to_IV = False
            is_quarter_from_II_to_I = False
            is_quarter_from_III_to_II = True
            is_quarter_from_IV_to_III = False
        
        # check if change quarter from II to I
        if check_if_negative(previous_x) and check_if_positive(current_x) and check_if_positive(previous_y) and check_if_positive(current_y):
            is_quarter_from_I_II = False
            is_quarter_from_II_to_III = False
            is_quarter_from_III_to_IV = False
            is_quarter_from_II_to_I = True
            is_quarter_from_III_to_II = False
            is_quarter_from_IV_to_III = False
        
        # check if change quarter from III to IV
        if check_if_negative(previous_x) and check_if_positive(current_x) and check_if_negative(previous_y) and check_if_negative(current_y):
            is_quarter_from_I_II = False
            is_quarter_from_II_to_III = False
            is_quarter_from_III_to_IV = True
            is_quarter_from_II_to_I = False
            is_quarter_from_III_to_II = False
            is_quarter_from_IV_to_III = False
        
        
        if is_quarter_from_II_to_III:
            list_of_theta1[i] = list_of_theta1[i] + 360.0
        
        if is_quarter_from_III_to_II:
            list_of_theta1[i] = list_of_theta1[i] - 360.0
            
        if is_quarter_from_III_to_IV:
            list_of_theta1[i] = list_of_theta1[i] + 360.0
            
        if is_quarter_from_II_to_I:
            list_of_theta1[i] = list_of_theta1[i] - 360.0
        
        # if has_zero_between(previous_x, current_x):
        #     if previous_x > current_x:
        #         has_x_went_from_plus_to_minus = True
        #         has_x_went_from_minus_to_plus = False
        #     else:
        #         has_x_went_from_plus_to_minus = False
        #         has_x_went_from_minus_to_plus = True
        
        # if has_x_went_from_minus_to_plus:
        #     list_of_theta1[i] = list_of_theta1[i] + 360.0
        
        # if has_x_went_from_plus_to_minus:
        #     list_of_theta1[i] = list_of_theta1[i] - 360.0
        
        
    return list_of_theta1, list_of_theta2, list_of_theta3

    


def bezier(X, Y, Z, speed):
    x, y, z = np.array([]), np.array([]), np.array([])

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

    theta1, theta2, theta3 = check_quarters_of_x(x,y,z)
    
    return x, y, z, theta1, theta2, theta3

# def bezier(numpy_notation_list,speed=0.01):
#     t_points = np.arange(0,2,speed)
#     correct_points = numpy_notation_list.T
#     curve = Bezier.Curve(t_points, correct_points)
#     return curve