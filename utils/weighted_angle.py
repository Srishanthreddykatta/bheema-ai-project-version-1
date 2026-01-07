import math
import numpy as np

def weighted_angle(p1, p2, p3):
    """Calculate angle between three points, weighted by visibility confidence."""
    x1, y1, z1, conf1 = p1.x, p1.y, p1.z, p1.visibility
    x2, y2, z2, conf2 = p2.x, p2.y, p2.z, p2.visibility
    x3, y3, z3, conf3 = p3.x, p3.y, p3.z, p3.visibility
    
    min_conf = min(conf1, conf2, conf3)
    
    v1 = np.array([x1 - x2, y1 - y2, z1 - z2])
    v2 = np.array([x3 - x2, y3 - y2, z3 - z2])
    
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
    cos_angle = np.clip(cos_angle, -1, 1)
    angle = math.degrees(math.acos(cos_angle))
    
    return angle, min_conf

def angle(p1, p2, p3):
    """Calculate angle between three points (for backward compatibility)."""
    angle_val, _ = weighted_angle(p1, p2, p3)
    return angle_val
