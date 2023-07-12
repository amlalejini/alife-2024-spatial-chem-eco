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

def gen_graph_toroidal_lattice(graph_width:int, graph_height:int):
    # return nx.toroidal_lattice_graph(nodes) # <-- Using the networkx generator
    graph = nx.Graph()
    # Create grid to use to figure out edges
    grid = [[None for c in range(graph_width)] for r in range(graph_height)]
    # Assign vertex ids to each position in grid
    id = 0
    for r in range(graph_height):
        for c in range(graph_width):
            grid[r][c] = id
            graph.add_node(id)
            id += 1
    # Compute edges
    for r in range(graph_height):
        for c in range(graph_width):
            id = grid[r][c]
            up = grid[r-1][c]
            down = grid[(r+1)%graph_height][c]
            right = grid[r][(c+1)%graph_width]
            left = grid[r][c-1]
            graph.add_edge(id, up)
            graph.add_edge(id, down)
            graph.add_edge(id, right)
            graph.add_edge(id, left)
    return graph

# Pseudo code at the momentd
def gen_graph_comet_kite(nodes:int, tails:int):
    # return nx.comet_kite_graph(nodes) # <-- Using the networkx generator
    graph = nx.complete_graph(nodes)
    for i in range(nodes):
        graph.add_nodes_from()
        graph.add_edges_from()
        for i in range(tails):
            graph.add_nodes_from()
            graph.add_edges_from()
    return graph

def gen_graph_circular_chain(nodes:int):
    # return nx.circular_chain_graph(nodes) # <-- Using the networkx generator
    graph = nx.path_graph(nodes)
    if nodes > 1:
        graph.add_edge(nodes - 1, 0)
    return graph

def gen_graph_linear_chain(nodes:int):
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(nodes)])
    graph.add_edges_from([(i,i + 1) for i in range(nodes-1)])
    return graph

def gen_graph_random_erdos_renyi(nodes:int,edge_prob:float, seed:int):
    # return nx.random_graph(nodes) # <-- Using the networkx generator
    graph = nx.erdos_renyi_graph(nodes, edge_prob, seed)
    print(graph.nodes)
    print(graph.edges)
    return graph

def gen_graph_random_barabasi_albert(nodes:int, edges:int, seed:int):
    # return nx.complete_graph(nodes) # <-- Using the networkx generator
    graph = nx.barabasi_albert_graph(nodes,edges, seed)
    return graph

def main():
    parser = argparse.ArgumentParser(
        usage="Program for generating graphs"
    )
    parser.add_argument(
        "--type",
        type = str,
        default = "well-mixed",
        choices = ["well-mixed", "toroidal-lattice", "comet-kite", "circular-chain", "linear-chain", "random-barabasi-albert", "random-erdos-renyi"],
        help = "Type of graph to generate"
    )
    parser.add_argument("--nodes", type = int, default = 10, help = "Number of nodes in graph")
    parser.add_argument("--tails", type = int, default = 2, help = "Number of tails conneted to graph")
    parser.add_argument("--height", type = int, default = 3, help = "Height of graph (for graph types where relevant)")
    parser.add_argument("--width", type = int, default = 3, help = "Width of the graph (for graph types where relevant)")
    parser.add_argument("--seed", type = int, default = 1, help = "Seed info")
    parser.add_argument("--edges", type = int, default =10, help = "Number of edges")
    parser.add_argument("--edge_probabilty", type = float, default = 0.5, help = "Edge creation probability")

    args = parser.parse_args()
    graph_type = args.type
    graph_nodes = args.nodes
    graph_tails = args.tails
    graph_width = args.width
    graph_height = args.height

    graph = None
    if graph_type == "well-mixed":
        graph = gen_graph_well_mixed(nodes = graph_nodes)
        print(graph)
    elif graph_type == "toroidal-lattice":
        graph = gen_graph_toroidal_lattice(graph_width=graph_width, graph_height=graph_height)
        print(graph)
    elif graph_type == "comet-kite":
        graph = gen_graph_comet_kite(nodes = graph_nodes)
        print(graph)
    elif graph_type == "circular-chain":
        graph = gen_graph_circular_chain(nodes = graph_nodes)
        print(graph)
    elif graph_type == "linear-chain":
        graph = gen_graph_linear_chain(nodes = graph_nodes)
        print(graph)
    elif graph_type == "random-barabasi-albert":
        graph = gen_graph_random_barabasi_albert(nodes = graph_nodes, edges = args.edges, seed = args.seed )
        print(graph)
    elif graph_type == "random-erdos-renyi":
        graph = gen_graph_random_erdos_renyi(nodes = graph_nodes, edge_prob = args.edge_prob, seed = args.seed)
        print(graph)
    else:
        print("Unrecognized graph type!")
        exit(-1)

if __name__ == '__main__':
    main()