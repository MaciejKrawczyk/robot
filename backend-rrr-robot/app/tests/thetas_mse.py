import numpy as np
import matplotlib.pyplot as plt

def read_data(filename):
    """
    Read the data from a text file and return it as a numpy array.
    """
    return np.loadtxt(filename, delimiter=',')

def calculate_mse(actual, target):
    """
    Calculate the Mean Square Error between actual and target values.
    """
    return np.mean((actual - target) ** 2)

def plot_data(time, actual, target, filename):
    """
    Plot actual and target angles over time.
    """
    plt.figure()
    plt.plot(time, actual, label='Actual Angles')
    plt.plot(time, target, label='Target Angles')
    plt.xlabel('Time')
    plt.ylabel('Angles')
    plt.title(f'Actual vs Target Angles for {filename}')
    plt.legend()
    plt.show()

def main():
    files = ['motor_data/2024-05-27_18-36-49_motor1_data.txt', 'motor_data/2024-05-27_18-36-49_motor2_data.txt', 'motor_data/2024-05-27_18-36-49_motor3_data.txt']
    
    
    for file in files:
        data = read_data(file)
        
        time = data[:, 0]
        actual_angles = data[:, 1]
        target_angles = data[:, 2]
        
        mse = calculate_mse(actual_angles, target_angles)
        print(f'Mean Square Error for {file}: {mse}')
        
        plot_data(time, actual_angles, target_angles, file)

if __name__ == "__main__":
    main()
