import math


def convert_to_degrees(theta_dict):
    for key in theta_dict:
        theta_dict[key] = math.degrees(theta_dict[key])
    return theta_dict