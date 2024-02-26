import heapq


def a_star_search(start_point, end_point, graph, eval_func):
    explored = []
    unexplored = []
    heapq.heapify(unexplored)
    for node in unexplored: pass

def evaluate_direct_distance(from_point: tuple, to_point: tuple):
    delta_x, delta_y = to_point[0] - from_point[0], to_point[1] - from_point[1]
    return int(pow(pow(delta_x, 2) + pow(delta_y, 2), 0.5))


if __name__ == '__main__':
    print(evaluate_direct_distance((3, 4),(5, 5)))
