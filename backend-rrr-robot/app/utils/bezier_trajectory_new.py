from types_global import PointXYZ, BezierControlPoints
from utils.kinematics import check_if_point_in_workspace_xyz, inverse_kinematics3, radians_to_degrees
import numpy as np
from utils.bezier_trajectory import check_quarters_of_x


def find_bezier_control_points(start: PointXYZ, end: PointXYZ) -> BezierControlPoints:
    """Find suitable control points for the Bézier curve."""
    
    vector = PointXYZ(end.x - start.x, end.y - start.y, end.z - start.z)

    control1 = PointXYZ(start.x + vector.x * 0.1,
                        start.y + vector.y * 0.1,
                        start.z + vector.z * 0.1)

    control2 = PointXYZ(start.x + vector.x * 0.9,
                        start.y + vector.y * 0.9,
                        start.z + vector.z * 0.9)

    if not check_if_point_in_workspace_xyz(control1) or not check_if_point_in_workspace_xyz(control2):
        raise ValueError("Generated control points are not in the workspace")

    return BezierControlPoints(start, control1, control2, end)


def bezier_formula(control_points: BezierControlPoints, t: float) -> PointXYZ:
    A, B, C, D = control_points.A, control_points.B, control_points.C, control_points.D
    x = (1 - t) ** 3 * A.x + 3 * (1 - t) ** 2 * t * B.x + 3 * (1 - t) * t ** 2 * C.x + t ** 3 * D.x
    y = (1 - t) ** 3 * A.y + 3 * (1 - t) ** 2 * t * B.y + 3 * (1 - t) * t ** 2 * C.y + t ** 3 * D.y
    z = (1 - t) ** 3 * A.z + 3 * (1 - t) ** 2 * t * B.z + 3 * (1 - t) * t ** 2 * C.z + t ** 3 * D.z
    point = PointXYZ(x, y, z)
    print(point)
    return point


def bezier_point(control_points: BezierControlPoints, t: float) -> PointXYZ:
    return bezier_formula(control_points, t)



def robot_trajectory(point1: PointXYZ, point2: PointXYZ):
    control_points = find_bezier_control_points(point1, point2)
    x, y, z = [], [], []
    theta1, theta2, theta3 = [], [], []

    for t in np.arange(0, 1.01, 0.01):  # Generate points every 0.01
        point = bezier_point(control_points, t)
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)
        thetas = inverse_kinematics3(point.x, point.y, point.z)
        theta1.append(radians_to_degrees(thetas.theta1))
        theta2.append(radians_to_degrees(thetas.theta2))
        theta3.append(radians_to_degrees(thetas.theta3))

    return x, y, z, theta1, theta2, theta3