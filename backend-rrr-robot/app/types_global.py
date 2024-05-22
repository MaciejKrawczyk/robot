class RobotPosition:
    def __init__(self, theta1: float, theta2: float, theta3: float, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y 
        self.z = z 
        self.theta1 = theta1
        self.theta2 = theta2
        self.theta3 = theta3
    
    def to_dict(self):
        return self.__dict__
    

class PointXYZ:
    def __init__(self, x: float, y: float, z: float):
        self.x = round(x, 5)
        self.y = round(y, 5)
        self.z = round(z, 5)

    def __str__(self):
        return f'PointXYZ: {self.x}, {self.y}, {self.z}'

    def to_dict(self):
        return self.__dict__

class PointThetas:
    def __init__(self, theta1: float, theta2: float, theta3: float):
        self.theta1 = round(theta1, 5)
        self.theta2 = round(theta2, 5)
        self.theta3 = round(theta3, 5)

    def __str__(self):
        return f'PointThetas: {self.theta1}, {self.theta2}, {self.theta3}'
    
    def to_dict(self):
        return self.__dict__
    
    
class BezierControlPoints:
    def __init__(self, A: PointXYZ, B: PointXYZ, C: PointXYZ, D: PointXYZ):
        self.A = A
        self.B = B
        self.C = C
        self.D = D