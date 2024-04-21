import numpy as np
from .helpers import pol2cart, cart2pol, radians_to_degrees

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