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

def check_quarters_of_x(list_of_x_values, list_of_y_values, list_of_z_values):
    
    is_quarter_from_I_II = False
    is_quarter_from_II_to_III = False
    is_quarter_from_III_to_IV = False
    is_quarter_from_II_to_I = False
    is_quarter_from_III_to_II = False
    is_quarter_from_IV_to_III = False
    
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

    # angles = np.array([inverse_kinematics_numpy(x[i], y[i], z[i]) for i in range(len(x))])
    
    # angles = np.array([inverse_kinematics_numpy(updated_x[i], updated_y[i], updated_z[i]) for i in range(len(x))])
    # theta1 = angles[:, 0]
    # theta2 = angles[:, 1]
    # theta3 = angles[:, 2]
    
    return x, y, z, theta1, theta2, theta3


points = np.array([
    [-1.59, -6.28, 16.57],
    [-8.78, 1.79, 22.12]
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

fig, axs = plt.subplots(3, 2, figsize=(10, 15))
# First row of plots
axs[0, 0].plot(np.linspace(0, 1, len(x)), theta1, 'b-')
axs[0, 0].set_title('Change of theta1 over time')
axs[0, 0].set_xlabel('t')
axs[0, 0].set_ylabel('theta1')

axs[0, 1].plot(np.linspace(0, 1, len(x)), x, 'b-')
axs[0, 1].set_title('Change of x over time')
axs[0, 1].set_xlabel('t')
axs[0, 1].set_ylabel('x')

# Second row of plots
axs[1, 0].plot(np.linspace(0, 1, len(y)), theta2, 'g-')
axs[1, 0].set_title('Change of theta2 over time')
axs[1, 0].set_xlabel('t')
axs[1, 0].set_ylabel('theta2')

axs[1, 1].plot(np.linspace(0, 1, len(y)), y, 'g-')
axs[1, 1].set_title('Change of y over time')
axs[1, 1].set_xlabel('t')
axs[1, 1].set_ylabel('y')

# Third row of plots
axs[2, 0].plot(np.linspace(0, 1, len(z)), theta3, 'r-')  # Adding the plot for theta3 here
axs[2, 0].set_title('Change of theta3 over time')
axs[2, 0].set_xlabel('t')
axs[2, 0].set_ylabel('theta3')

axs[2, 1].plot(np.linspace(0, 1, len(z)), z, 'r-')
axs[2, 1].set_title('Change of z over time')
axs[2, 1].set_xlabel('t')
axs[2, 1].set_ylabel('z')

# Set grid and adjust layout
for ax_row in axs:
    for ax in ax_row:
        ax.grid(True)

plt.tight_layout()
plt.show()

# Save the figure with a timestamp
file_name = f'app/tests/{time.strftime("%d_%m_%Y_%H_%M_%S")}_test_plot_bezier.png'
plt.savefig(file_name)
print(f"Saved as {file_name}")