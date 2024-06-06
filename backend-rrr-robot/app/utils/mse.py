import os

def calculate_mean_square_error(directory, filenames):
    mse_values = []

    for i, filename in enumerate(filenames):
        filepath = os.path.join(directory, filename)
        actual_angles, target_angles = [], []
        
        with open(filepath, 'r') as file:
            for line in file:
                time_point, actual_angle, target_angle, pid_output, error = line.strip().split(',')
                actual_angles.append(float(actual_angle))
                target_angles.append(float(target_angle))

        if len(actual_angles) != len(target_angles):
            raise ValueError("The lengths of actual angles and target angles do not match.")

        # Calculate mean square error
        mse = sum((actual - target) ** 2 for actual, target in zip(actual_angles, target_angles)) / len(actual_angles)
        mse_values.append(mse)

    return mse_values

# Example usage
directory = 'motor_data'
filenames = ['2024-05-27_18-36-49_motor1_data.txt', '2024-05-27_18-36-49_motor2_data.txt', '2024-05-27_18-36-49_motor3_data.txt']
mse_values = calculate_mean_square_error(directory, filenames)
for i, mse in enumerate(mse_values):
    print(f"Mean Square Error for {filenames[i]}: {mse}")