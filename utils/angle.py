import math
import numpy as np

def calculate_angle(p1, p2, p3):
    """Calculate angle between three points."""
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    
    v1 = np.array([x1 - x2, y1 - y2])
    v2 = np.array([x3 - x2, y3 - y2])
    
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
    cos_angle = np.clip(cos_angle, -1, 1)
    angle = math.degrees(math.acos(cos_angle))
    
    return angle
