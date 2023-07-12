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
import random
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

# Algorithm from "Exploring and mapping the universe of evolutionary graphs
# identifies structural properties affecting fixation and probability time"
# (Moller et al)
# TODO
# - Add random number seed, set random number seed
# - Write out the behavior of this function as a comment
def gen_graph_comet_kite(core_size:int, num_tails:int, additional_tail_nodes:int = 0, seed:int = 1):
    # return nx.comet_kite_graph(nodes) # <-- Using the networkx generator
    random.seed(seed)
    # 1) Generate complete graph
    graph = nx.complete_graph(core_size)
    # If no nodes, return empty graph
    if core_size < 1:
        return graph
    # 2) Pick existing node to attach tail
    tail_root = 0
    # 3) Attach t ("tails") nodes to the tail_root node
    tail_nodes = [t for t in range(core_size, core_size + num_tails)]
    graph.add_nodes_from(tail_nodes)
    graph.add_edges_from([(tail_root, t) for t in tail_nodes])
    if len(tail_nodes) < 1:
        return graph
    # 4) Attach any additional tail nodes to existing tails
    for i in range(additional_tail_nodes):
        attach_point = random.choice(tail_nodes)
        new_node = core_size + num_tails + i
        graph.add_node(new_node)
        graph.add_edge(attach_point, new_node)
        tail_nodes.append(new_node)
    # print("Core nodes:", graph.nodes)
    # print("Initial tail nodes:", tail_nodes)
    # print("Edges: ", graph.edges)
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
    parser.add_argument("--additional_tail_nodes", type = int, default = 2, help = "Number of nodes in tail part of graph")
    parser.add_argument("--height", type = int, default = 3, help = "Height of graph (for graph types where relevant)")
    parser.add_argument("--width", type = int, default = 3, help = "Width of the graph (for graph types where relevant)")
    parser.add_argument("--seed", type = int, default = 1, help = "Seed info")
    parser.add_argument("--edges", type = int, default =10, help = "Number of edges")
    parser.add_argument("--edge_probabilty", type = float, default = 0.5, help = "Edge creation probability")

    args = parser.parse_args()
    graph_type = args.type
    graph_nodes = args.nodes
    graph_tails = args.tails
    graph_additional_tail_nodes = args.additional_tail_nodes
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
        graph = gen_graph_comet_kite(
            core_size = graph_nodes,
            num_tails = graph_tails,
            additional_tail_nodes = graph_additional_tail_nodes,
            seed = args.seed
        )
        print(graph)
    elif graph_type == "circular-chain":
        graph = gen_graph_circular_chain(nodes = graph_nodes)
        print(graph)
    elif graph_type == "linear-chain":
        graph = gen_graph_linear_chain(nodes = graph_nodes)
        print(graph)
    elif graph_type == "random-barabasi-albert":
        graph = gen_graph_random_barabasi_albert(nodes = graph_nodes, edges = args.edges, seed = args.seed)
        print(graph)
    elif graph_type == "random-erdos-renyi":
        graph = gen_graph_random_erdos_renyi(nodes = graph_nodes, edge_prob = args.edge_prob, seed = args.seed)
        print(graph)
    else:
        print("Unrecognized graph type!")
        exit(-1)

if __name__ == '__main__':
    main()