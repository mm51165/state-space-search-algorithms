import sys


class Node:

    def __init__(self, name, cost, parent, path, heruistic_value=0):
        self.name = name
        self.cost = cost
        self.parent = parent
        self.path = path
        self.heuristic_value = heruistic_value


# Unimplemented recursive path finding using parent node
def find_path(final, s0, path, cost):
    if final.name == s0:
        path.append(s0)
        return path, cost

    path.append(final.name)
    parent = final.parent
    cost += float(final.cost)
    return find_path(parent, s0, path, cost)


def bfs(s0, succ, goal):
    open = []
    node = Node(s0, 0, None, [s0])
    open.append(node)
    visited = []
    all = []

    while open:
        n = open.pop(0)
        visited.append(n)
        for ret in goal:
            if ret.strip() == n.name:
                return visited, n.path, n.cost
        for m in succ[n.name]:
            new_path = [*n.path, m[0]]
            new_node = Node(m[0], n.cost + float(m[1]), n, new_path)
            open.append(new_node)
            all.append(new_node)

    return None, None, None, None


def ucs(s0, succ, goal):
    open = []
    node = Node(s0, 0, None, [s0])
    open.append(node)

    visited = []

    while open:
        n = open.pop(0)
        visited.append(n)
        for ret in goal:
            if ret.strip() == n.name:
                return visited, n.path, n.cost
        for m in succ[n.name]:
            new_path = [*n.path, m[0]]
            new_node = Node(m[0], float(m[1]) + n.cost, n, new_path)
            open.append(new_node)

        open.sort(key=lambda tup: (float(tup.cost), tup.name))

    return None, None, None, None


def astar(s0, succ, goal, h):
    open = []
    node = Node(s0, 0, None, [s0])
    closed = []

    while open:
        n = open.pop(0)
        for ret in goal:
            if ret.strip() == n.name:
                return visited, n.path, n.cost

        closed.append(n)
        for m in succ[n.name]:
            pass


def read_ss(state_space):
    s0 = None
    goal = None
    state = None

    unsorted = []
    state_dict = {}

    f = open(state_space, 'r')
    for line in f.readlines():
        split_line = line.split(':')
        if len(split_line) == 1 and not line.startswith('#'):
            if s0:
                goal = [g.strip() for g in line.split(' ')]
            else:
                s0 = line.strip()

        elif not line.startswith('#'):
            for argument in split_line:
                split_argument = argument.split(' ')
                for value in split_argument:
                    split_value = value.split(',')
                    if len(split_value) == 1 and split_value[0] and split_value[0] != "\n":
                        state = split_value[0].strip()
                        state_dict[state] = []
                    elif value and split_value[0] != "\n":
                        state_dict[state].append((value.split(',')[0].strip(), value.split(',')[1].rstrip()))

    for key in state_dict:
        state_dict[key].sort(key=lambda place: place[0])

    return s0, goal, state_dict


if __name__ == '__main__':
    n, states_visited, path, total_cost = None, None, None, None
    algoritm = sys.argv[sys.argv.index('--alg') + 1]
    state_space = sys.argv[sys.argv.index('--ss') + 1]

    s0, goal, state_dict = read_ss(state_space)

    node_serializer = lambda nodes: [node.name for node in nodes]

    if algoritm == 'bfs':

        print("# BFS")
        visited, path, cost = bfs(s0, state_dict, goal)
        visited = set(node_serializer(visited))
        n = True


    elif algoritm == 'ucs':

        print("# UCS")
        visited, path, cost = ucs(s0, state_dict, goal)
        visited = set(node_serializer(visited))
        n = True
    else:
        heuristic = sys.argv[sys.argv.index('--h') + 1]

    if n:
        print('[FOUND_SOLUTION]:', 'yes')
        print('[STATES_VISITED]:', len(visited))
        print('[PATH_LENGTH]:', len(path))
        print('[TOTAL_COST]:', cost)
        print('[PATH]:', ' => '.join(path))

    else:
        print('[FOUND_SOLUTION]:', 'no')
