"""
Programmer: John Shea
Project: Spatial Structure
Date: 06/30/2023
Version: 1

Reference
NetworkX
Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart,
“Exploring network structure, dynamics, and function using NetworkX”,
 in Proceedings of the 7th Python in Science Conference (SciPy2008),
 Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008
"""
import argparse
import networkx as nx

def gen_graph_well_mixed(nodes:int):
    # return nx.complete_graph(nodes) # <-- Using the networkx generator
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(nodes)])
    graph.add_edges_from([(j, i) for i in range(nodes) for j in range(i) if i != j])
    return graph
    pass

def gen_graph_toroidal_lattice(nodes:int,rows:int,cols:int):
    # return nx.toroidal_lattice_graph(nodes) # <-- Using the networkx generator
    graph = nx.Graph()
    graph.add_nodes_from((i, j) for i in range(nodes) for j in range(nodes))
    return graph

def gen_graph_comet_kite(nodes:int):
    # return nx.comet_kite_graph(nodes) # <-- Using the networkx generator
    graph = nx.complete_graph(nodes)
    # graph.add_nodes_from([i for i in range(nodes)])
    # graph.add_edges_from([(j, i) for i in range(nodes) for j in range(i) if i != j])
    return graph

def gen_graph_circular_chain(nodes:int):
    # return nx.circular_chain_graph(nodes) # <-- Using the networkx generator
    graph = nx.DiGraph()
    start_node = nodes[]
    graph.add_edges_from(start_node)
    print(graph)


def gen_graph_linear_chain(nodes:int):
    # return nx.linear_chain_graph(nodes) # <-- Using the networkx generator
    graph = nx.Graph()
    graph.add_edges_from([(i, i + 1) for i in range(nodes - 1)])
    graph.add_edges_from([(i, i + 1) for i in range(nodes, 2 * nodes - 1)])
    graph.add_edges_from([(i, i + nodes) for i in range(nodes)])
    return graph


def gen_graph_random_erdos_renyi(nodes:int,edge_prob:float):
    # return nx.random_graph(nodes) # <-- Using the networkx generator
    n = int(input("input the number of nodes:"))
    edge_prob = float(input("input the edge building probability as a float:"))
    graph = nx.erdos_renyi_graph(nodes, edge_prob)
    print(graph.nodes)
    print(graph.edges)
    pass


def gen_graph_random_barabasi_albert(nodes:int, edges:int, seed:float):
    # return nx.complete_graph(nodes) # <-- Using the networkx generator
    n = int(input("input the number of nodes:"))
    m = int(input("input the number of edges to attach from a new node to existing nodes"))
    seed = int(input("input randomness as integer"))
    graph = nx.barabasi_albert_graph(n,m,seed)
    return graph
    pass

def main():
    parser = argparse.ArgumentParser(
        usage="Program for generating graphs"
    )
    parser.add_argument("--type", type = str, default = "circular chain", choices = ["well-mixed", "toroidal lattice", "comet-kite", "circular chain", "linear chain", "barabasi-albert random", "erdos-renyi random"], help = "Type of graph to generate")
    parser.add_argument("--nodes", type = int, default = 10, help = "Number of nodes in graph")
    parser.add_argument("--rows", type = int, default = 10, help = "Number of rows in graph")
    parser.add_argument("--cols", type=int, default=10, help="Number of columns in graph")

    args = parser.parse_args()
    graph_type = args.type
    graph_nodes = args.nodes

    graph = None
    if graph_type == "well-mixed":
        graph = gen_graph_well_mixed(nodes = graph_nodes)
        print(graph)
    elif graph_type == "toroidal lattice":
        graph = gen_graph_toroidal_lattice(nodes = graph_nodes, rows=10, cols=10)
        print(graph)
    elif graph_type == "comet-kite":
        graph = gen_graph_comet_kite(nodes = graph_nodes)
        print(graph)
    elif graph_type == "circular chain":
        graph = gen_graph_circular_chain(nodes = graph_nodes)
        print(graph)
    elif graph_type == "linear chain":
        graph = gen_graph_linear_chain(nodes = graph_nodes)
        print(graph)
    elif graph_type == "barabasi-albert random":
        graph = gen_graph_random_barabasi_albert(nodes = graph_nodes, edges=5, seed=0.5)
        print(graph)
    elif graph_type == "erdos-renyi random":
        graph = gen_graph_random_erdos_renyi(nodes = graph_nodes, edge_prob=float)
        print(graph)
    else:
        print("Unrecognized graph type!")
        exit(-1)


if __name__ == '__main__':
    main()