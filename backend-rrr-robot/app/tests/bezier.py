import numpy as np
import matplotlib.pyplot as plt
import time


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


def bezier(X, Y, Z, speed):
    # Convert lists to numpy arrays
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    
    # Initialize empty arrays for the output coordinates
    x = np.array([])
    y = np.array([])
    z = np.array([])
    
    # Loop through every four points to calculate bezier curves
    for i in range(0, len(X) - 1, 3):
        # Ensure there are enough points for the last segment
        if i + 3 >= len(X):
            break
        
        # Define the control points
        p0 = np.array([X[i], Y[i], Z[i]])
        p1 = np.array([X[i+1], Y[i+1], Z[i+1]])
        p2 = np.array([X[i+2], Y[i+2], Z[i+2]])
        p3 = np.array([X[i+3], Y[i+3], Z[i+3]])
        
        # Generate t values
        t = np.arange(0, 1 + speed, speed)
        
        # Calculate the bezier curve for each dimension
        curve_x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
        curve_y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
        curve_z = (1 - t)**3 * p0[2] + 3 * (1 - t)**2 * t * p1[2] + 3 * (1 - t) * t**2 * p2[2] + t**3 * p3[2]
        
        # Concatenate the new curve points to the existing arrays
        x = np.concatenate([x, curve_x])
        y = np.concatenate([y, curve_y])
        z = np.concatenate([z, curve_z])
    
    return x, y, z


points = np.array([
    [0, 0, 32],
    [-8.98, -0.14, 23.65],
    [-0.92, -0.1, 31.95],
    [-5.27, 6.46, 26.39]
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
x, y, z = bezier(X, Y, Z, 0.01)
ax.plot3D(x, y, z, 'go-', label='Bézier Curve')
ax.legend()

# New figure for changes over time
fig, axs = plt.subplots(3, 1, figsize=(10, 15))
axs[0].plot(np.linspace(0, 1, len(x)), x, 'r-')
axs[0].set_title('Change of x over time')
axs[0].set_xlabel('t')
axs[0].set_ylabel('x')

axs[1].plot(np.linspace(0, 1, len(y)), y, 'g-')
axs[1].set_title('Change of y over time')
axs[1].set_xlabel('t')
axs[1].set_ylabel('y')

axs[2].plot(np.linspace(0, 1, len(z)), z, 'b-')
axs[2].set_title('Change of z over time')
axs[2].set_xlabel('t')
axs[2].set_ylabel('z')

for ax in axs:
    ax.grid(True)

plt.tight_layout()
plt.show()
plt.savefig(f'app/tests/{time.strftime("%H_%M_%S", time.localtime())}_test_plot_bezier.png')