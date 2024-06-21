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

def plot_error(time, error, ax, title):
    """
    Plot error over time with red line and small square markers.
    """
    ax.plot(time, error, 'r-s', label='Error', markersize=5)
    ax.set_xlabel('Time')
    ax.set_ylabel('Error')
    ax.set_title(title)
    ax.legend()

def main():
    files = ['motor_data/2024-05-27_18-36-49_motor1_data.txt', 
             'motor_data/2024-05-27_18-36-49_motor2_data.txt', 
             'motor_data/2024-05-27_18-36-49_motor3_data.txt']
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    for i, file in enumerate(files):
        data = read_data(file)
        
        time = data[:, 0]
        actual_angles = data[:, 1]
        target_angles = data[:, 2]
        
        mse = calculate_mse(actual_angles, target_angles)
        print(f'Mean Square Error for {file}: {mse}')
        
        error = actual_angles - target_angles
        plot_error(time, error, axs[i], f'Error for {file}')

    plt.tight_layout()
    plt.savefig('errors_xyz')
    plt.show()

if __name__ == "__main__":
    main()
