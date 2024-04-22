import math
from .helpers import radians_to_degrees


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

    return {"x": x, "y": y, "z": z}


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

        angles = {"theta1": radians_to_degrees(theta1), "theta2": radians_to_degrees(theta2), "theta3": radians_to_degrees(theta3)}
        return angles
    
