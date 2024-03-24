from __future__ import annotations
import math
from typing import Dict, List, Tuple

DOTAREA = 10



class GraphVertex:
    idcounter = 1
    default_cost = 5

    def distance_to(self, pos: Tuple[float, float]) -> float:
        x1, y1 = self.pos[0], self.pos[1]
        x2, y2 = pos[0], pos[1]
        dx = x1 - x2
        dy = y1 - y2
        return math.sqrt(dx * dx + dy * dy)


    def rec_check(self, sup: GraphVertex):
        if self in sup.visited:
            return True
        sup.visited.append(self)
        for ch in self.children:
            if ch.rec_check(sup):
                return True
        sup.visited.remove(self)
        return False

    def check_is_cyclicality(self) -> bool:
        self.visited = [self]
        for ch in self.children:
            if ch.rec_check(self):
                return True
        
        del self.visited
        return False
        # visited: List[GraphVertex] = [self]
        # qu: List[GraphVertex] = list(self.children)
        # while qu:
        #     ver = qu.pop(0)
        #     if ver in visited:
        #         return True
        #     visited.append(ver)
        #     qu = list(ver.children) + qu
        # return False

    def connect(self, other: GraphVertex, cost: int):
        self.children.add(other)
        if self.check_is_cyclicality():
            self.children.remove(other)
            return
        self.costs[other] = cost

    def disconnect(self, other: GraphVertex):
        self.children.remove(other)
        del self.costs[other]

    def is_dot_interaction(self, pos: Tuple[float, float]) -> bool:
        return self.distance_to(pos) < DOTAREA

    def middle(self, other: GraphVertex) -> Tuple[float, float]:
        x = (self.pos[0] + other.pos[0]) / 2
        y = (self.pos[1] + other.pos[1]) / 2
        return (x,y)

    def __init__(self, pos: tuple) -> None:
        self.id = GraphVertex.idcounter
        GraphVertex.idcounter += 1
        self.pos = pos
        self.children: set[GraphVertex] = set()
        self.costs: Dict[GraphVertex, int] = {}

