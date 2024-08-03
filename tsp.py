import numpy as np

def create_distance_matrix(coordinates):
    """Creates a distance matrix from coordinates."""
    return np.array([[int(np.linalg.norm(c1 - c2)) for c2 in coordinates] for c1 in coordinates])

def minimum_spanning_tree(distance_matrix):
    """Finds the Minimum Spanning Tree using Prim's algorithm."""
    n = len(distance_matrix)
    selected = [False] * n
    min_edge = [(float('inf'), -1)] * n
    min_edge[0] = (0, -1)
    mst = []
    
    for _ in range(n):
        v = min((w, idx) for idx, (w, sel) in enumerate(min_edge) if not selected[idx])[1]
        selected[v] = True
        if min_edge[v][1] != -1:
            mst.append((v, min_edge[v][1]))
        for to in range(n):
            if distance_matrix[v][to] < min_edge[to][0]:
                min_edge[to] = (distance_matrix[v][to], v)
    return mst

def adjacency_list(mst):
    """Converts edge list to adjacency list."""
    adj_list = {}
    for u, v in mst:
        adj_list.setdefault(u, []).append(v)
        adj_list.setdefault(v, []).append(u)
    return adj_list

def root(tree):
    """Finds root nodes in the tree nodes with one connection."""
    return [node for node, neighbors in tree.items() if len(neighbors) == 1]

def dfs(node, tree, tour, visited):
    """Performs Depth-First Search (DFS) to generate a tour."""
    visited[node] = True
    tour.append(node)
    for neighbor in tree[node]:
        if not visited[neighbor]:
            dfs(neighbor, tree, tour, visited)

def tour_cost(tour, distance_matrix):
    """Calculates the cost of a given tour."""
    return sum(int(distance_matrix[tour[i]][tour[(i+1)%len(tour)]]) for i in range(len(tour)))

def construct_tour(distance_matrix):
    """Constructs an initial tour using MST and DFS."""
    mst = minimum_spanning_tree(distance_matrix)
    sorted(mst, key=lambda x: distance_matrix[x[0]][x[1]])
    tree = adjacency_list(mst)
    root_nodes = root(tree)
    best_tour = list(range(len(distance_matrix)))
    for node in root_nodes:
        visited = [False] * len(distance_matrix)
        tour = []
        dfs(node, tree, tour, visited)
        if tour_cost(tour, distance_matrix) < tour_cost(best_tour, distance_matrix):
            best_tour = tour
    return best_tour

def tour_optimization(tour, distance_matrix):
    """Performs 2-opt optimization on the given tour."""
    n = len(distance_matrix)
    r = np.argsort(distance_matrix, axis=1)
    p = np.argsort(r, axis=1)
    y = np.argsort(tour)

    flag = True
    while flag:
        flag = False
        for i in range(n):
            n_ = p[tour[i], tour[(i + 1) % n]]
            for j_ in range(1, n_):
                j = y[r[tour[i], j_]]
                if i == j:
                    continue
                delta = (distance_matrix[tour[i], tour[j]] + distance_matrix[tour[(i + 1) % n], tour[(j + 1) % n]] -
                         distance_matrix[tour[i], tour[(i + 1) % n]] - distance_matrix[tour[j], tour[(j + 1) % n]])
                if delta < 0:
                    if j < i:
                        i, j = j, i
                    tour[i + 1:j + 1] = tour[i + 1:j + 1][::-1]
                    y = np.argsort(tour)
                    flag = True
    return tour

def tsp(coordinates):
    """Solves the TSP problem using the Double-Tree Short Cutting and 2-Opt Heuristic Algorithm."""
    distance_matrix = create_distance_matrix(coordinates)
    optimal_tour = construct_tour(distance_matrix)
    optimized_tour = tour_optimization(optimal_tour, distance_matrix)
    new_coordinates = [coordinates[i].tolist() for i in optimized_tour]
    return new_coordinates