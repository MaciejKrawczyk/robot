import numpy as np
import math
import matplotlib.pyplot as plt
import time

def degrees_to_radians(degrees: float):
    radians = degrees * (math.pi / 180)
    return radians


def radians_to_degrees(radians: float):
    degrees = radians * (180 / np.pi)
    return degrees


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


    # if  (L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3) < -1  or (r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2) < -1:
    #     theta1 = theta1 + 180
    # elif (L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3) > 1 or (r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2) > 1:
    #     theta1 = theta1 - 180

    angles = [
        radians_to_degrees(theta1),
        radians_to_degrees(theta2),
        radians_to_degrees(theta3)
    ]
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

    angles = [
        radians_to_degrees(theta1),
        radians_to_degrees(theta2),
        radians_to_degrees(theta3)
    ]
    return angles


# def bezier(X, Y, Z, speed):
#     x, y, z = np.array([]), np.array([]), np.array([])

#     for i in range(0, len(X) - 1, 3):
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

#     angles = np.array([inverse_kinematics_numpy(x[i], y[i], z[i]) for i in range(len(x))])
#     theta1 = angles[:, 0]
#     theta2 = angles[:, 1]
#     theta3 = angles[:, 2]
    
#     return x, y, z, theta1, theta2, theta3


# def bezier(X, Y, Z, speed):
#     x, y, z = np.array([]), np.array([]), np.array([])
#     previous_point = None  # Initialize the previous point as None
#     prev_angles = None  # Placeholder to store previous angles

#     for i in range(0, len(X) - 1, 3):
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

#     angles = []
#     is_theta1_jump_plus = False
#     is_theta1_jump_minus = False
#     for i in range(len(x)):
#         current_point = np.array([x[i], y[i], z[i]])
#         current_angles = inverse_kinematics_numpy_2(x[i], y[i], z[i])
#         # current_angles_before_modifications = current_angles.copy()
#         if previous_point is not None and prev_angles is not None:
#             # Here we add comparisons between prev_angles and current_angles
#             # You will fill in the logic you want to handle inside these if statements
#             if current_angles[0] - prev_angles[0] < -350:
#                 print('Adjustment needed for theta1 < -200')
#                 current_angles[0] = current_angles[0] - 360.0
#                 # if is_theta1_jump_plus is True:
#                 #     is_theta1_jump_minus = False
#                 #     is_theta1_jump_plus = False
                
#             if current_angles[0] - prev_angles[0] > 170:
#                 print('Adjustment needed for theta1 > 150')
#                 # current_angles[0] = current_angles[0] + 360.0
#                 # is_theta1_jump_plus = True
#                 # is_theta1_jump_minus = False
#             # Add more conditions as needed
            
#         if is_theta1_jump_plus is True:
#             # current_angles[0] = current_angles[0] - 360.0
#             pass

#         if is_theta1_jump_minus is True:
#             # current_angles[0] = current_angles[0] + 360.0
#             pass

#         angles.append(current_angles)
#         previous_point = current_point  # Update the previous point
#         prev_angles = current_angles  # Update the previous angles

#         angles = np.array(angles)
#         theta1 = angles[:, 0]
#         theta2 = angles[:, 1]
#         theta3 = angles[:, 2]

#     return x, y, z, theta1, theta2, theta3

def bezier(X, Y, Z, speed):
    x, y, z = np.array([]), np.array([]), np.array([])
    prev_angles = None  # Placeholder to store previous angles

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

    angles = []
    for i in range(len(x)):
        current_point = np.array([x[i], y[i], z[i]])
        current_angles = np.array(inverse_kinematics_numpy_2(x[i], y[i], z[i]))
        if prev_angles is not None:
            angle_differences = current_angles - prev_angles
            # Correct angle jumps greater than 180 degrees
            for j in range(len(current_angles)):
                if angle_differences[j] > 180:
                    current_angles[j] -= 360
                elif angle_differences[j] < -180:
                    current_angles[j] += 360

        angles.append(current_angles)
        prev_angles = current_angles  # Update the previous angles

    angles = np.array(angles)
    theta1, theta2, theta3 = angles.T

    return x, y, z, theta1, theta2, theta3



points = np.array([
    [0, 0, 32],
    [-8.97, -0.42, 23.6],
    [-0.79, 0.0, 31.97],
    [-1.37, -8.26, 26.3]
]).T  # Transpose to match MATLAB's format

# Extract the initial x, y, z coordinates
x0, y0, z0 = points

# Plot initial points
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot3D(x0, y0, z0, 'ko-', label='Initial Points')
ax.set_title('Initial and Bézier Curve')

# Add points and plot them
X, Y, Z = add_points(points, 1)
ax.plot3D(X[0], X[1], X[2], 'ro-', label='Refined Points')

# Generate and plot Bézier curve
x, y, z, theta1, theta2, theta3 = bezier(X, Y, Z, 0.01)
ax.plot3D(x, y, z, 'go-', label='Bézier Curve')
ax.legend()

# New figure for changes over time
fig, axs = plt.subplots(3, 1, figsize=(10, 15))
axs[0].plot(np.linspace(0, 1, len(x)), theta1, 'b-')
axs[0].set_title('Change of theta1 over time')
axs[0].set_xlabel('t')
axs[0].set_ylabel('theta1')

axs[1].plot(np.linspace(0, 1, len(y)), theta2, 'g-')
axs[1].set_title('Change of theta2 over time')
axs[1].set_xlabel('t')
axs[1].set_ylabel('theta2')

axs[2].plot(np.linspace(0, 1, len(z)), theta3, 'b-')
axs[2].set_title('Change of theta3 over time')
axs[2].set_xlabel('t')
axs[2].set_ylabel('theta3')

for ax in axs:
    ax.grid(True)

plt.tight_layout()
plt.show()
plt.savefig(f'app/tests/{time.strftime("%d_%m_%H_%M_%S", time.localtime())}_test_plot_bezier.png')