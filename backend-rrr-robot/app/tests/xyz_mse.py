import numpy as np
import matplotlib.pyplot as plt

# Function to read the data from a text file
def read_data(file_path):
    data = np.loadtxt(file_path, delimiter=',')
    return data

# Function to calculate the Mean Square Error for each axis
def calculate_mse(data):
    actual_x = data[:, 0]
    target_x = data[:, 3]
    actual_y = data[:, 1]
    target_y = data[:, 4]
    actual_z = data[:, 2]
    target_z = data[:, 5]

    mse_x = np.mean((actual_x - target_x) ** 2)
    mse_y = np.mean((actual_y - target_y) ** 2)
    mse_z = np.mean((actual_z - target_z) ** 2)
    
    return mse_x, mse_y, mse_z

# Function to plot the MSE for each axis
def plot_mse(mse_x, mse_y, mse_z):
    axes = ['X', 'Y', 'Z']
    mse_values = [mse_x, mse_y, mse_z]
    print(mse_x)
    print(mse_y)
    print(mse_z)

    plt.bar(axes, mse_values, color=['red', 'green', 'blue'])
    plt.xlabel('Axis')
    plt.ylabel('Mean Square Error')
    plt.title('Mean Square Error for Each Axis')
    plt.savefig('xyz_mse')
    plt.show()

# Main script
file_path = 'parsed_angles.txt'  # Replace with your file path
data = read_data(file_path)
mse_x, mse_y, mse_z = calculate_mse(data)
plot_mse(mse_x, mse_y, mse_z)
