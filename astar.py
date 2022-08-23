#! /usr/bin/python3

from pyray import *
import math
from time import sleep
import time

WIN_WIDTH = 600
WIN_HEIGHT = 480

MAP_SIZE = 30
TILE_SIZE = 10

the_map = []

for i in range(MAP_SIZE):
    the_map.append([False] * MAP_SIZE)

a_wall = [
    [14, 13],
    [14, 14],
    [14, 15],
    [15, 13],
    [16, 13],
    [17, 13],
    [9, 10],
    [10, 10],
    [11, 10]
]


for y in range(5, 23):
    for x in range(5, 23):
        a_wall.append([x, y])


for x in range(5, MAP_SIZE):
    a_wall.append([x, 5])


for i in a_wall:
    the_map[i[1]][i[0]] = True



class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, p):
        return self.x == p.x and self.y == p.y



class Node:

    def __init__(self, pos):
        self.pos = pos
        self.parent = None
        self.id = time.time()

        self.g = 0
        self.h = 0
        self.f = 0


    def set_f(self):
        self.f = self.g + self.h


    def __eq__(self, other):
        return self.pos == other.pos


    def copy(self):
        new_node = Node(self.pos)
        new_node.g = self.g
        new_node.h = self.h
        new_node.f = self.f
        return new_node



def get_dis(p1, p2):
    return int(math.hypot(p2.x - p1.x, p2.y - p1.y) * 10)


the_open_nodes = []
the_closed_nodes = []

def find_path(start, end):
    global the_open_nodes, the_closed_nodes

    open_nodes = []
    close_nodes = []

    # Set first node.
    new_node = Node(start)
    new_node.g = 0
    new_node.h = get_dis(start, end)
    new_node.set_f()
    open_nodes.append(new_node)

    while len(open_nodes) > 0:
        curr_node = open_nodes[0]

        # Get best node.
        for n in open_nodes:
            if n.f < curr_node.f:
                curr_node = n

        open_nodes.remove(curr_node)
        close_nodes.append(curr_node)

        #print(f"{curr_node.pos.x} {curr_node.pos.y}")

        # At end.
        if curr_node.pos == end:
            path = []

            current = curr_node

            while current is not None:
                path.append(current.pos)
                current = current.parent

            the_open_nodes = open_nodes.copy()
            the_closed_nodes = close_nodes.copy()
            return path

        # Create children.
        for y in range(-1, 2):
            for x in range(-1, 2):
                new_x = curr_node.pos.x + x
                new_y = curr_node.pos.y + y

                if x == 0 and y == 0:
                    continue

                if new_x >= MAP_SIZE or new_x < 0:
                    continue
                if new_y >= MAP_SIZE or new_y < 0:
                    continue

                if the_map[new_y][new_x]:
                    continue

                # Create new node
                new_node = Node(Point(new_x, new_y))
                new_node.parent = curr_node
                new_node.g = curr_node.g + get_dis(curr_node.pos, new_node.pos)
                new_node.h = get_dis(new_node.pos, end)
                new_node.set_f()

                in_closed = False

                # In closed nodes.
                for closed_child in close_nodes:
                    if new_node == closed_child:
                        in_closed = True
                        break

                if in_closed:
                    continue

                in_open = False

                # In open nodes.
                for open_child in open_nodes:
                    if new_node == open_child:
                        in_open = True
                        break

                if in_open:
                    continue

                open_nodes.append(new_node)


    return None



def main():
    init_window(WIN_WIDTH, WIN_HEIGHT, "Test")
    set_target_fps(60)

    start_time = time.time()
    points = find_path(Point(0, 0), Point(27, 10))

    print(f"Time: {time.time() - start_time}")

    while not window_should_close():
         

        begin_drawing()
        clear_background(RAYWHITE)

        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                if the_map[y][x]:
                    draw_rectangle(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, BLACK)
                else:
                    draw_rectangle(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, YELLOW)

        for p in points:
            draw_rectangle(p.x * TILE_SIZE, p.y * TILE_SIZE, TILE_SIZE, TILE_SIZE, BLUE)

        for n in the_open_nodes:
            draw_rectangle(n.pos.x * TILE_SIZE, n.pos.y * TILE_SIZE, TILE_SIZE, TILE_SIZE, Color(0xff, 0xff, 0xff, 0x7f))
        for n in the_closed_nodes:
            draw_rectangle(n.pos.x * TILE_SIZE, n.pos.y * TILE_SIZE, TILE_SIZE, TILE_SIZE, Color(0x00, 0x00, 0xff, 0x7f))

        end_drawing()

    close_window()

    print(f"close size: {len(the_closed_nodes)}, open size: {len(the_open_nodes)}, num of tiles: {MAP_SIZE * MAP_SIZE}")


if __name__ == "__main__":
    main()
