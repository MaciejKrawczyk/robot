import numpy as np
import matplotlib.pyplot as plt
import math


def degrees_to_radians(degrees):
    """
    Convert degrees to radians.

    Parameters:
    degrees (float): Angle in degrees.

    Returns:
    float: Angle in radians.
    """
    radians = degrees * (math.pi / 180)
    return radians


def IK(theta1: float, theta2: float, theta3: float, l1=14, l2=9, l3=9):
    """
    wg mojej implementacji
    # thetas not in degrees, in radians!!!!
    """
    
    
    theta1_radians = degrees_to_radians(theta1)
    theta2_radians = degrees_to_radians(theta2)
    theta3_radians = degrees_to_radians(theta3)
    
    # theta1_radians = theta1
    # theta2_radians = theta2
    # theta3_radians = theta3
    
    
    a3 = l3
    a2 = l2
    h1 = l1

    c23 = math.cos(theta2_radians + theta3_radians)
    s23 = math.sin(theta2_radians + theta3_radians)
    c2 = math.cos(theta2_radians)
    s2 = math.sin(theta2_radians)
    c1 = math.cos(theta1_radians)
    s1 = math.sin(theta1_radians)

    x = c1 * (a3 * c23 + a2 * c2)
    y = s1 * (a3 * c23 + a2 * c2)
    z = a3 * s23 + a2 * s2 + h1

    return x,y,z
# File names for input and output
input_files = [
    'motor_data/2024-05-27_18-36-49_motor1_data.txt',
    'motor_data/2024-05-27_18-36-49_motor2_data.txt', 
    'motor_data/2024-05-27_18-36-49_motor3_data.txt'
    ]
output_filename = 'parsed_angles.txt'

# Initialize lists to hold the parsed angles
parsed_actual_angles = []
parsed_target_angles = []

# Read the data from each file
data = [[] for _ in range(7)]  # time, actual_theta1, target_theta1, actual_theta2, target_theta2, actual_theta3, target_theta3

for i, filename in enumerate(input_files):
    with open(filename, 'r') as file:
        for line in file:
            columns = line.strip().split(',')
            if i == 0:  # First file, initialize the data list with time and theta1 values
                data[0].append(float(columns[0]))  # time
                data[1].append(float(columns[1]))  # actual_theta1
                data[2].append(float(columns[2]))  # target_theta1
            elif i == 1:  # Second file, append theta2 values
                data[3].append(float(columns[1]))  # actual_theta2
                data[4].append(float(columns[2]))  # target_theta2
            elif i == 2:  # Third file, append theta3 values
                data[5].append(float(columns[1]))  # actual_theta3
                data[6].append(float(columns[2]))  # target_theta3

# Ensure all data lists have the same length
min_length = min(len(data[0]), len(data[1]), len(data[2]), len(data[3]), len(data[4]), len(data[5]), len(data[6]))
data = [d[:min_length] for d in data]

# Apply IK function to each set of angles and store the results
for i in range(min_length):
    actual_angles = IK(data[1][i], data[3][i], data[5][i])
    target_angles = IK(data[2][i], data[4][i], data[6][i])
    parsed_actual_angles.append(actual_angles)
    parsed_target_angles.append(target_angles)

# Write the parsed angles to a new file
with open(output_filename, 'w') as file:
    for actual_angle, target_angle in zip(parsed_actual_angles, parsed_target_angles):
        file.write(f"{actual_angle[0]},{actual_angle[1]},{actual_angle[2]},{target_angle[0]},{target_angle[1]},{target_angle[2]}\n")

print(f"Parsed angles written to {output_filename}")


# Create the plots
time = data[0]
actual_theta1 = [angles[0] for angles in parsed_actual_angles]
target_theta1 = [angles[0] for angles in parsed_target_angles]
actual_theta2 = [angles[1] for angles in parsed_actual_angles]
target_theta2 = [angles[1] for angles in parsed_target_angles]
actual_theta3 = [angles[2] for angles in parsed_actual_angles]
target_theta3 = [angles[2] for angles in parsed_target_angles]

fig, axs = plt.subplots(3, 1, figsize=(10, 15))

# Plot theta1
axs[0].plot(time, actual_theta1, label='Actual X', color='blue')
axs[0].plot(time, target_theta1, label='Target X', color='red', linestyle='--')
axs[0].set_title('X')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Position')
axs[0].legend()
axs[0].grid(True)

# Plot theta2
axs[1].plot(time, actual_theta2, label='Actual Y', color='blue')
axs[1].plot(time, target_theta2, label='Target Y', color='red', linestyle='--')
axs[1].set_title('Y')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('Position')
axs[1].legend()
axs[1].grid(True)

# Plot theta3
axs[2].plot(time, actual_theta3, label='Actual Z', color='blue')
axs[2].plot(time, target_theta3, label='Target Z', color='red', linestyle='--')
axs[2].set_title('Z')
axs[2].set_xlabel('Time')
axs[2].set_ylabel('Position')
axs[2].legend()
axs[2].grid(True)

# Adjust layout
plt.tight_layout()
plt.savefig('angles_plot.png')
plt.show()