from utils.angle import calculate_angle
from utils.angle import calculate_angle

def weighted_angle(a, b, c):
    angle = calculate_angle(
        (a.x, a.y),
        (b.x, b.y),
        (c.x, c.y)
    )
    confidence = min(a.visibility, b.visibility, c.visibility)
    return angle, confidence
