import math
from .helpers import radians_to_degrees, degrees_to_radians
from types_global import PointXYZ, PointThetas
from config import config




def forward_kinematics(theta1: float, theta2: float, theta3: float, l1=14, l2=9, l3=9):
    """
    wg mojej implementacji
    # thetas not in degrees, in radians!!!!
    """
    
    
    # theta1_radians = degrees_to_radians(theta1)
    # theta2_radians = degrees_to_radians(theta2)
    # theta3_radians = degrees_to_radians(theta3)
    
    theta1_radians = theta1
    theta2_radians = theta2
    theta3_radians = theta3
    
    
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

    position = PointXYZ(x, y, z)
    return position


def inverse_kinematics3(x, y, z, l1=14, l2=9, l3=9):
    """
    elbow down
    wg filmiku z yt https://www.youtube.com/watch?v=Jj5pqbQWKuE CORRECT!!!!!
    """
    h = l1
    L1 = l2
    L2 = l3

    theta1 = math.atan2(y, x)  #
    r2 = z - h  
    r1 = math.sqrt(x ** 2 + y ** 2) 
    r3 = math.sqrt(r1 ** 2 + r2 ** 2) 
    fi1 = math.atan2(r2, r1)  
    fi2 = math.acos((L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3)) 
    theta2 = fi2 + fi1  
    fi3 = math.acos((r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2)) 
    theta3 = fi3 - math.pi 

    angles = PointThetas(theta1, theta2, theta3)
    return angles
    
    
def inverse_kinematics2( x, y, z, l1=14, l2=9, l3=9):
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
    fi1 = math.acos((L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3))  #
    theta2 = fi2 - fi1  # 2
    fi3 = math.acos((r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2))  #
    theta3 = math.pi - fi3  #

    # angles = {"theta1": theta1, "theta2": theta2, "theta3": theta3}
    # return angles
    angles = PointThetas(theta1, theta2, theta3)
    return angles



def check_if_point_in_workspace_thetas(point: PointThetas):
    return (config['THETA1_RANGES'][0] < point.theta1 < config['THETA1_RANGES'][1] and
            config['THETA2_RANGES'][0] < point.theta2 < config['THETA2_RANGES'][1] and
            config['THETA3_RANGES'][0] < point.theta3 < config['THETA3_RANGES'][1])


def check_if_point_in_workspace_xyz(point: PointXYZ):
    point_thetas_from_kinematics = inverse_kinematics3(point.x, point.y, point.z)
    # print(point_thetas_from_kinematics.theta1, point_thetas_from_kinematics.theta2, point_thetas_from_kinematics.theta3)
    point_thetas = PointThetas(point_thetas_from_kinematics.theta1,
                               point_thetas_from_kinematics.theta2,
                               point_thetas_from_kinematics.theta3)
    return check_if_point_in_workspace_thetas(point_thetas)