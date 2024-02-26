import heapq


def a_star_search(start_point, end_point, graph, eval_func):
    explored = []
    unexplored = []
    heapq.heapify(unexplored)
    for node in unexplored: pass


def evaluate_direct_distance(from_point: tuple, to_point: tuple):
    delta_x, delta_y = to_point[0] - from_point[0], to_point[1] - from_point[1]
    return int(pow(pow(delta_x, 2) + pow(delta_y, 2), 0.5))


def graph_from_grid(width, length):
    graph = {}
    for x in range(width):
        for y in range(length):
            graph[x, y] = [(x, y) for x, y in ((x-1, y-1), (x, y-1), (x+1, y-1),
                                             (x-1, y), (x+1, y),
                                             (x-1, y+1), (x, y+1), (x+1, y+1))
                           if width > x >= 0 and length > y >= 0]
    return graph



if __name__ == '__main__':
    print(evaluate_direct_distance((3, 4),(5, 5)))
    print(graph_from_grid(3,3))
