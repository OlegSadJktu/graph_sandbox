from sys import set_coroutine_origin_tracking_depth
from typing import Tuple
from utils import dot_hypo, hypo


class Line:
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float]) -> None:
        self.start = start
        self.end = end

    def __getitem__(self, key: float) -> tuple[float, float]:
        x = self.end[0] - self.start[0]
        y = self.end[1] - self.start[1]
        size = hypo(x,y)
        k = 0
        if size != 0:
            k = (size + key) / size
        newx = x * k
        newy = y * k
        return newx + self.start[0], newy + self.start[1]


    def perpendiculars(self) -> list[Tuple[float, float]]:
        x = self.end[0] - self.start[0]
        y = self.end[1] - self.start[1]
        first = (-y + self.start[0], x + self.start[1])
        second = (y + self.start[0], -x + self.start[1])
        return [first, second]


    def belongs(self, dot: Tuple[int, int], blur = 5) -> bool:
        x1, y1 = self.start
        x2, y2 = self.end
        x3, y3 = dot
        x = (x1 * x1 * x3 - 2 * x1 * x2 * x3 + x2 * x2 * x3 + x2 *
            (y1 - y2) * (y1 - y3) - x1 * (y1 - y2) * (y2 - y3)) / ((x1 - x2) *
                    (x1 - x2) + (y1 - y2) * (y1 - y2))
        y = (x2 * x2 * y1 + x1 * x1 * y2 + x2 * x3 * (y2 - y1) - x1 *
            (x3 * (y2 - y1) + x2 * (y1 + y2)) + (y1 - y2) * (y1 - y2) * y3) / ((
                        x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
        distance = dot_hypo((x, y), dot)
        in_range = (x1 < x and x2 > x) or (x1 > x and x2 < x)
        return (distance <= blur) and in_range
