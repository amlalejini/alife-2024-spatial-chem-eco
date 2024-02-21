import networkx as nx
import os

def read_graph_matrix(file_path:str, directed=False):
    '''
    Read graph saved in matrix format
    '''
    content = None
    with open(file_path, "r") as fp:
        content = fp.read().strip().split("\n")
    matrix = [list(map(int, line.strip().split(","))) for line in content]
    is_square = all([len(row) == len(matrix) for row in matrix])
    if not is_square:
        print("Matrix not square.")
        raise RuntimeError
    graph = nx.Graph() if not directed else nx.DiGraph()
    # Add nodes
    graph.add_nodes_from([i for i in range(len(matrix))])
    # Add edges between nodes
    for row_i in range(len(matrix)):
        row = matrix[row_i]
        for col_i in range(len(row)):
            if row[col_i] > 0:
                graph.add_edge(row_i, col_i)
    return graph


