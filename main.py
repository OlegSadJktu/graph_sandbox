from typing import List, Mapping, Tuple
import pygame 
from pygame.color import THECOLORS
import sys
import graph_vertex as gv
from line import Line

BACKGROUNDCOLOR = THECOLORS['white']
VERTEXCOLOR = THECOLORS['orange']

VERTEXRAD = 25
WIDTH, HEIGHT = 1280, 800
FPS = 60

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("arial", 25)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

counter = 0
clock = pygame.time.Clock()


vertexes: List[gv.GraphVertex] = [
        gv.GraphVertex((200, 200)),
        gv.GraphVertex((400, 200))
        ]



def find_by_pos(pos: tuple) -> gv.GraphVertex | None:
    for ver in vertexes:
        if ver.distance_to(pos) < VERTEXRAD:
            return ver


class Edge:
    def __init__(self, a: Tuple[float, float], b: Tuple[float, float], source: gv.GraphVertex) -> None:
        self.a = a
        self.b = b
        self.source = source

selected: gv.GraphVertex | None = None
dragable: gv.GraphVertex | None = None
edge: Edge | None = None


class Costs:
    def __init__(self):
        self.costs: dict[Tuple[int, int], int] = {}

    def get(self, key: list[int]) -> int:
        if len(key) != 2:
            return 0
        sor = list(key)
        sor.sort()
        return self.costs[tuple(sor)]

    def unset(self, key: list[int]):
        if len(key) != 2:
            return 0
        sor = list(key)
        sor.sort()
        del self.costs[tuple(sor)]


    def set(self, key: list[int], value: int):
        if len(key) != 2:
            return 0
        sor = list(key)
        sor.sort()
        self.costs[tuple(sor)] = value
        





def vertex_by_id(i: int) -> gv.GraphVertex | None:
    for ver in vertexes:
        if ver.id == i:
            return ver

def vertex_pair_by_id(pair: Tuple[int, int]) -> Tuple[gv.GraphVertex | None, gv.GraphVertex | None]:
    return (vertex_by_id(pair[0]), vertex_by_id(pair[1]))

def shortest_way(src: gv.GraphVertex, dest: gv.GraphVertex) -> list[int]:
    parents: dict[gv.GraphVertex, gv.GraphVertex] = {x: src for x in src.children}
    prices = {x: src.costs[x] for x in src.children}
    visited: list[gv.GraphVertex] = []

    def find_lowest_node_cost():
        m: int | None = None
        ret: gv.GraphVertex | None = None
        for key, value in prices.items():
            if ((m is None) or m < value) and key not in visited:
                m = value
                ret = key
        return ret

    def get_cost(ver: gv.GraphVertex) -> float:
        if ver in prices:
            return prices[ver]
        return float('inf')
    
    node = find_lowest_node_cost()
    while node is not None:
        cost = prices[node]
        for ch in node.children:
            ch_cost = get_cost(ch)
            from_node_cost = node.costs[ch]
            new_cost = from_node_cost + cost
            if new_cost < ch_cost:
                prices[ch] = int(new_cost)
                parents[ch] = node
        visited.append(node)
        node = find_lowest_node_cost()

    if not parents.get( dest ):
        return []
   
    ret: list[int] = []
    ver = dest
    while ver is not None:
        ret.insert(0, ver.id)
        ver = parents.get( ver )
    return ret

src_dest: list[gv.GraphVertex] = []

def add_vertex(a: gv.GraphVertex):
    global src_dest
    src_dest.append(a)
    if len(src_dest) > 2:
        src_dest = src_dest[-2:]

state_is_changed: bool = False
way: list[int] = []

def print_text(pos: Tuple[int, int], t: str):
    text = font.render(t, False, THECOLORS['black'])
    textRect = text.get_rect()
    textRect.center = (pos[0], pos[1] - VERTEXRAD - 18)
    screen.blit(text, textRect)


while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        counter += 1
        r = pygame.Rect(counter, counter, 200, 200)
        screen.fill(THECOLORS['white'])

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            if pressed[0]:
                if selected is not None and selected.is_dot_interaction(pos):
                    edge = Edge(selected.pos, pos, selected)

                else:
                    dragable = selected

            if pressed[2]:
                vertexes.append(gv.GraphVertex(pos))
            if pressed[1]:
                ver = find_by_pos(pos)
                if ver is not None:
                    add_vertex(ver)
                    state_is_changed = True
                    



        elif event.type == pygame.MOUSEWHEEL:
            pos = pygame.mouse.get_pos()
            for ver in vertexes:
                for other, value in ver.costs.items():
                    line = Line(ver.pos, other.pos)
                    if line.belongs(pos, 20):
                        step = event.y
                        value += step
                        value = max([value, 1])
                        value = min([value, 15])
                        ver.costs[other] = value
                        state_is_changed = True

        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            ver = find_by_pos(pos)
            selected = ver
            if dragable is not None: 
                dragable.pos = pos
            if edge is not None: 
                edge.b = pos

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if edge is not None:
                ver = find_by_pos(pos)
                if edge.source != ver and ver is not None:
                    edge.source.connect(ver, 5)
                    state_is_changed = True

            if dragable is not None: 
                if dragable.pos[0] < 50 and dragable.pos[1] < 50:
                    vertexes.remove( dragable )
                    if dragable in src_dest:
                        src_dest.remove(dragable)
                    for ch in list(dragable.children):
                        dragable.disconnect(ch)
                        state_is_changed = True

            dragable = None
            edge = None

        if state_is_changed:
            if len(src_dest) == 2:
                way = shortest_way(src_dest[0], src_dest[1]);
                if not way: 
                    way = shortest_way(src_dest[1], src_dest[0]);
            else:
                way = []
            state_is_changed = False


        for ver in vertexes:
            rad, w = VERTEXRAD, 3
            if selected == ver:
                if ver.distance_to(pygame.mouse.get_pos()) < 10:
                    pygame.draw.circle(screen, THECOLORS['black'], ver.pos, 4)
                else:
                    rad += 3
                    w += 3

            # for ch in ver.children:
            #     cost = costs.get([ch.id, ver.id])
            print_text(ver.pos, str(ver.id))
            pygame.draw.circle(screen, THECOLORS['orange'], ver.pos, rad, w)
            if ver in src_dest:
                pygame.draw.circle(screen, THECOLORS['green'], ver.pos, rad + 8, w)


        for ver in vertexes:
            for other, value in ver.costs.items():
                if other not in ver.children:
                    print('impossible')
                    exit(1)
                first = ver
                second = other
                pos = first.middle(second)
                print_text(tuple(map(int, pos)), str(value))
                line = Line(first.pos, second.pos)
                eol = line[-VERTEXRAD]
                line = Line(first.pos, eol)
                cutted = Line(line[-value * 3], line.end)

                if line.belongs(pygame.mouse.get_pos(), 20):
                    col = 'magenta'
                else: 
                    col = 'black';
                if ver.id in way:
                    ver_ind = way.index(ver.id)
                    if len(way) > ver_ind + 1 and way[ver_ind+1] == other.id:
                        col = 'red'
                tip = cutted.perpendiculars()
                points = tip + [line.end]
                pygame.draw.line(screen, THECOLORS[col], line.start, line.end, value)
                pygame.draw.polygon(screen, THECOLORS[col], points)



        if edge is not None:
            pygame.draw.line(screen, THECOLORS['red'], edge.a, edge.b, 5)

        if dragable is not None:
            pygame.draw.rect(screen, THECOLORS['red'], (0,0, 50, 50), 5)

        pygame.display.update()


