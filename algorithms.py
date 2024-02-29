import heapq

def evaluate_direct_distance(from_point: tuple, to_point: tuple):
    delta_x, delta_y = to_point[0] - from_point[0], to_point[1] - from_point[1]
    return pow(pow(delta_x, 2) + pow(delta_y, 2), 0.5)


def graph_from_grid(width, length):
    graph = {}
    for x in range(width):
        for y in range(length):
            graph[x, y] = [(x, y) for x, y in ((x, y-1), (x-1, y), (x+1, y), (x, y+1))
                           if width > x >= 0 and length > y >= 0]
    return graph


def a_star_search(start_point, end_point, graph, eval_func=evaluate_direct_distance,
                  *, additional_constraints_to_successors=None):
    explored = []
    unexplored = []
    heapq.heapify(unexplored)

    def successors_of_node(node):
        return (successor for successor in graph[node]
                if all(constraint_check(successor)
                       for constraint_check in (lambda x: x not in explored, additional_constraints_to_successors)
                       if constraint_check))

    heapq.heappush(unexplored, (eval_func(start_point, end_point), [start_point]))
    while unexplored:
        value, path = heapq.heappop(unexplored)
        last_path_node = path[-1]
        if last_path_node == end_point:
            return path
        if last_path_node in explored:
            continue
        for successor in successors_of_node(last_path_node):
            further_path = path[:]
            further_path.append(successor)
            successor_value = len(path) - 1 + eval_func(successor, end_point)  # find f(x) = g(x) + h(x) of successor
            heapq.heappush(unexplored, (successor_value, further_path))
        explored.append(last_path_node)
    return None






if __name__ == '__main__':
    print(evaluate_direct_distance((3, 4), (5, 5)))
    graph = graph_from_grid(5, 5)
    path = a_star_search((0,0), (2, 3), graph)
    print(path)
