config = {
    'ENABLE_HOLDING_THREAD': True,
    'IMAGES_DIRECTORY': "/home/maciek/Desktop/robot/backend-rrr-robot/motor_plots",
    'ARM_LENGTHS': {
        'L1': 14,
        'L2': 9,
        'L3': 9,
    },
    'THETA1_RANGES': (0, 180),
    'THETA2_RANGES': (-45, 90),
    'THETA3_RANGES': (-135, 0)
}

class ArmLengths:
    def __init__(self) -> None:
        self.L1 = 14
        self.L2 = 9
        self.L3 = 9

class Config:
    def __init__(self) -> None:
        self.ENABLE_HOLDING_THREAD = True
        self.ARM_LENGTHS = ArmLengths
        self.THETA1_RANGES = (0, 180)
        self.THETA2_RANGES = (-45, 90)
        self.THETA3_RANGES = (-135, 0)
