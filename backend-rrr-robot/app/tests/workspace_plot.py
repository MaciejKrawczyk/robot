import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

# Define the joint limits in degrees
joint_limits_deg = [(0, 360), (-45, 90), (-90, 0)]

# Convert joint limits to radians
joint_limits = [(np.radians(l), np.radians(u)) for l, u in joint_limits_deg]

# Lengths of the arms
lengths = [14, 9, 9]

def forward_kinematics(theta1: float, theta2: float, theta3: float, l1=14, l2=9, l3=9):
    """
    wg mojej implementacji
    thetas not in degrees, in radians!!!!
    """
    
    a3 = l3
    a2 = l2
    h1 = l1

    c23 = math.cos(theta2 + theta3)
    s23 = math.sin(theta2 + theta3)
    c2 = math.cos(theta2)
    s2 = math.sin(theta2)
    c1 = math.cos(theta1)
    s1 = math.sin(theta1)

    x = c1 * (a3 * c23 + a2 * c2)
    y = s1 * (a3 * c23 + a2 * c2)
    z = a3 * s23 + a2 * s2 + h1

    return x, y, z

# Generate angles within their limits
num_samples = 50
theta1_vals = np.linspace(*joint_limits[0], num_samples)
theta2_vals = np.linspace(*joint_limits[1], num_samples)
theta3_vals = np.linspace(*joint_limits[2], num_samples)

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

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='r', marker='o', s=0.1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Workspace of the RRR Manipulator')
plt.savefig('fdasfasdfdas')
plt.show()
