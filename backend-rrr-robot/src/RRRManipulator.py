import math
from utils import convert_to_degrees
import asyncio


class Motor:
    def __init__(self, range_max: float, range_min: float):
        self.range_max = range_max
        self.range_min = range_min
        self.current_angle = 0

    async def rotate(self, angle: float):
        while self.current_angle != angle:
            if self.current_angle < angle:
                self.current_angle += 1
                # print(self.current_angle)
                await asyncio.sleep(0.01)
            else:
                self.current_angle -= 1
                # print(self.current_angle)
                await asyncio.sleep(0.01)

    def calibrate(self):
        """ calibrates the motor to the 0 position """
        # self.current_angle = 0
        pass


class RRRManipulator:
    def __init__(self, l1: float, l2: float, l3: float, motor_alfa: Motor, motor_beta: Motor, motor_gamma: Motor):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.motor_alfa = motor_alfa
        self.motor_beta = motor_beta
        self.motor_gamma = motor_gamma
        self.current_position = {"x": 0, "y": 0, "z": 0}
        self.current_angles = {"alfa": 0, "beta": 0, "gamma": 0}
        self.current_position['x'] = self.forward_kinematics(self.current_angles['alfa'], self.current_angles['beta'], self.current_angles['gamma'])['x']
        self.current_position['y'] = self.forward_kinematics(self.current_angles['alfa'], self.current_angles['beta'], self.current_angles['gamma'])['y']
        self.current_position['z'] = self.forward_kinematics(self.current_angles['alfa'], self.current_angles['beta'], self.current_angles['gamma'])['z']
        self.step = 0.1  # step for manual movement!
        # print(self.current_position)
        # print(self.current_angles)

    def calibrate(self):
        """ calibrates the motors to the 0 position """
        self.motor_alfa.calibrate()
        self.motor_beta.calibrate()
        self.motor_gamma.calibrate()

    def forward_kinematics(self, alfa: float, beta: float, gamma: float):
        """ wg mojej implementacji """
        a3 = self.l3
        a2 = self.l2
        h1 = self.l1

        c23 = math.cos(beta + gamma)
        s23 = math.sin(beta + gamma)
        c2 = math.cos(beta)
        s2 = math.sin(beta)
        c1 = math.cos(alfa)
        s1 = math.sin(alfa)

        x = c1 * (a3 * c23 + a2 * c2)
        y = s1 * (a3 * c23 + a2 * c2)
        z = a3 * s23 + a2 * s2 + h1

        return {"x": x, "y": y, "z": z}

    def inverse_kinematics_final(self, x, y, z, degrees=False):
        """ based on outputs uses the correct inverse kinematics function """

        inv1 = self.inverse_kinematics2(x, y, z)
        if inv1['theta2'] < -math.pi / 2 or inv1['theta2'] > 3 * math.pi / 2:
            result = self.inverse_kinematics2(x, y, z)
        else:
            result = inv1

        return convert_to_degrees(result) if degrees else result

    def inverse_kinematics2(self, x, y, z, degrees=False):
        """
        wg filmiku z yt https://www.youtube.com/watch?v=D93iQVoSScQ
        elbow up
        """

        h = self.l1
        L1 = self.l2
        L2 = self.l3

        theta1 = math.atan2(y, x)  # 1
        r2 = z - h  # 4
        r1 = math.sqrt(x ** 2 + y ** 2)  #
        r3 = math.sqrt(r1 ** 2 + r2 ** 2)  #
        fi2 = math.atan2(r2, r1)  # 3
        fi1 = math.acos((L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3))  #
        theta2 = fi2 - fi1  # 2
        fi3 = math.acos((r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2))  #
        theta3 = math.pi - fi3  #

        angles = {"theta1": theta1, "theta2": theta2, "theta3": theta3}
        return convert_to_degrees(angles) if degrees else angles

    def inverse_kinematics3(self, x, y, z, degrees=False):
        """
        elbow down
        wg filmiku z yt https://www.youtube.com/watch?v=Jj5pqbQWKuE CORRECT!!!!!
        """
        h = self.l1
        L1 = self.l2
        L2 = self.l3

        theta1 = math.atan2(y, x)  # 1
        r2 = z - h  # 4
        r1 = math.sqrt(x ** 2 + y ** 2)  #
        r3 = math.sqrt(r1 ** 2 + r2 ** 2)  #
        fi1 = math.atan2(r2, r1)  # 3
        fi2 = math.acos((L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3))  #
        theta2 = fi2 + fi1  # 2
        fi3 = math.acos((r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2))  #
        theta3 = fi3 - math.pi  #

        angles = {"theta1": theta1, "theta2": theta2, "theta3": theta3}
        return convert_to_degrees(angles) if degrees else angles

    def move_alfa(self, angle: float):
        self.motor_alfa.rotate(angle)

    def move_beta(self, angle: float):
        self.motor_beta.rotate(angle)

    def move_gamma(self, angle: float):
        self.motor_gamma.rotate(angle)

    def move_x(self):
        pass

    def move_y(self):
        pass

    def move_z(self):
        pass

    def move_to_point(self, x, y, z):
        pass


if __name__ == "__main__":
    motor_alfa = Motor(range_max=360, range_min=0)
    motor_beta = Motor(range_max=270, range_min=0)
    motor_gamma = Motor(range_max=270, range_min=0)
    rrr = RRRManipulator(l1=1, l2=1, l3=1, motor_alfa=motor_alfa, motor_beta=motor_beta, motor_gamma=motor_gamma)