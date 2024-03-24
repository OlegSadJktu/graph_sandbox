
import math
from typing import Tuple


def dot_hypo(a: Tuple[float, float], b: Tuple[float, float]):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return hypo(dx, dy)

def hypo(a, b):
    return math.sqrt(a * a + b * b)
