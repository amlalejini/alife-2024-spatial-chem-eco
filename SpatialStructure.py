"""
Programmer: Alex Lalejini, John Shea
Project: Spatial Structure
Date: 06/30/2023
Version: 1

Reference
NetworkX
Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart,
“Exploring network structure, dynamics, and function using NetworkX”,
 in Proceedings of the 7th Python in Science Conference (SciPy2008),
 Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008

Experiment sizes
well-mixed: 
--nodes 100
toroidal-lattice: height x width
height 10
width 10
comet-kite:
--coresize 40 
--tail-size 20
--additional-tails 40
linear-chain: 
--nodes 100
barabasi: 
--nodes 100 
--edges 10
waxman:
--nodes 100
--beta 0.4
--alpha 0.2
 
"""

import argparse
import random
import networkx as nx

def gen_graph_well_mixed(nodes:int):
    """
    Function generates a well-mixed graph where all nodes are connected by edges.
    Attributes:
        nodes(int): Indicates the number of nodes input by user. 
    Returns:
        The well-mixed graph based on the number of nodes and edges connecting the nodes. 
    """
    #Generates an empty graph. 
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(nodes)])
    graph.add_edges_from([(j, i) for i in range(nodes) for j in range(i) if i != j])
    return graph

def gen_graph_toroidal_lattice(graph_width:int, graph_height:int):
    """
    Function generates a toroidal lattice graph. 
    Attributes:
        graph_width(int): Indicates the width of the lattice domain. 
        graph_height(int): Indicates the height of the lattice domain.
    Returns:
        The toroidal graph based number of nodes and edges. 
    """
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
    """
    Function generates a comet-kite graph. 
    Attributes:
        core_size(int): The number of nodes that make up the comet 'core' structure.
        num_tails(int): The number of tails that connect to the comet 'core' structure. 
        additional_tail_nodes(int): The randomly assigned node connections that are added to the length of a comet tail. 
        seed(int): Integer value used to intialize a pseudorandom generator.
    Returns:
        The comet-kite graph based on the number of nodes and edges. 
    """
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
    """
    Function generates a cyclic graph. 
    Attributes:
        nodes(int): The indicated number of nodes within the cyclic graph. 
    Returns:
        The cyclic graph based number of nodes and edges. 
    """
    graph = nx.path_graph(nodes)
    if nodes > 1:
        graph.add_edge(nodes - 1, 0)
    return graph

def gen_graph_linear_chain(nodes:int):
    """
    Function generates a linear chain or path graph. 
    Attributes:
        nodes(int): The indicated number of nodes in the linear chain graph. 
    Returns:
        The linear chain based number of nodes and edges. 
    """
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(nodes)])
    graph.add_edges_from([(i,i + 1) for i in range(nodes-1)])
    return graph

def gen_graph_star(nodes:int):
    """
    Function generates a star graph. 
    Attributes:
        nodes(int): The indicated number of nodes in the star.  
    Returns:
        A star shaped graph. More of a spoke though. (?)
    """
    graph = nx.star_graph(nodes)
    return graph 


def gen_graph_random_erdos_renyi(nodes:int,edge_prob:float, seed:int):
    """
    Function that generates a random graph structure.  
    Attributes:
        nodes(int): The indicated number of nodes that in the random structure. 
        edge_prob(float): Represents the probability an edge will be created between nodes. 
        seed(int): Positive integer that intializes a random number generator.
    Returns:
        
    """
    graph = nx.erdos_renyi_graph(nodes, edge_prob, seed)
    print(graph.nodes)
    print(graph.edges)
    return graph

def gen_graph_random_barabasi_albert(nodes:int, edges:int, seed:int):
    """
    Function generates a random graph structure.  
    Attributes:
        nodes(int): The indicated number of nodes that will make up the random graph structure. 
        edges(int): The indicated number of edges that will connect a new node to an existing node. 
        seed(int): Positive integer that intializes a random number generator.
    Returns:
         A random graph structure. 
    """
    graph = nx.barabasi_albert_graph(nodes, edges, seed)
    return graph

def gen_graph_random_waxman(nodes:int, beta:float, alpha:float, seed:int):
    """
    Function generates a random graph structure.  
    Attributes:
        nodes(int): The indicated number of nodes included in the random graph structure.
        beta(float): Model parameter needed for random waxman graph generator. 
        alpha(float): Model parameter needed for random waxman graph generator. 
        seed(int): Positive integer that intializes a random number generator.
    Returns:
        A random graph structure.
    """
    graph = nx.waxman_graph(n=nodes,beta=beta,alpha=alpha,seed=seed)
    return graph

def gen_graph_random_geometric(nodes:int, radius:float, dimension:int, seed:int ):
    """
    Function generates a random geometric graph. Based on the workings of Penrose.  
    Attributes:
        nodes(int): The indicated number of nodes included in the random graph structure.
        radius(float): 
        dimension(int):
        seed(int): Positive integer that intializes a random number generator.
    Returns:
        The a random graph structure based on the parameters of 
    """
    graph = nx.random_geometric_graph()
    return graph

def gen_graph_edge_swapping(type:str, nodes:int ):
    """
    Function
    -Takes any graph as input
    -No edges connecting nodes of degree 3 to nodes of degree 4
    -Two edges are randomly selected to be disconnected
    -Nodes that are parallel with respect to the two disconnected edgess are then connected
    --after rewiring: two edges connecting nodes of degree 3 to nodes of degree 4 (no longer 4 clique)
    Checks:
    degree of distribution is preserved 
    >>mixing patterns of nodes changed
    pearson
    fully connected or not
    Attributes:
    Returns:
    """
    #Graph type input
    #1. Two edges randomly selected
    #2. Parallel edges are connected
    #graph_type = input()
    #for nodes in range(graph_input):
    #random.choice(nodes)
    #if nodes == 3 and neighboring_node == 4:
    #graph.remove_edges_from(node, neigbhoring_node)
    #graph.add_edges_from(node_degree, neighbor_node_degree)
    pass

def write_undirected_graph_to_edges_csv(fname:str, graph:nx.Graph):
    file_content = "" # Will contain output to write to file
    lines = []        # Will be a list of csv rows to write to file

    # We need to track which nodes are represented in the edge list.
    # It is possible that there are nodes with no connections that we'll
    # need to add to the end of the file.
    nodes_represented = set()

    # Loop over edges in graph, creating the line that will be added to the file
    for edge in graph.edges:
        from_node = edge[0]
        to_node = edge[1]
        # Add from --> to
        lines.append(f"{from_node},{to_node}")
        # Add to --> from (because this is an undirected graph;
        #  if this were a directed graph, would not want this line of code)
        lines.append(f"{to_node},{from_node}")
        # Make note of which nodes we've encountered
        nodes_represented.add(from_node)
        nodes_represented.add(to_node)

    # Any nodes not encountered by looping over edges (i.e., nodes that have no edges),
    # we need to add as lines to the file indicating that it is a part of the graph
    for node in graph.nodes:
        if not node in nodes_represented:
            lines.append(f"{node},NONE")

    # Combine lines with header information to create file content
    header = "from,to"
    file_content += header + "\n"
    file_content += "\n".join(lines)
    # Write file content to file
    with open(fname, "w") as fp:
        fp.write(file_content)

def main():
    parser = argparse.ArgumentParser(
        usage="Program for generating graphs"
    )
    parser.add_argument(
        "--type",
        type = str,
        default = "well-mixed",
        choices = ["well-mixed", "toroidal-lattice", "comet-kite", "circular-chain", "linear-chain", "random-barabasi-albert", "random-erdos-renyi", "random-waxman", "random-geometric", "edge-swapping", "star"],
        help = "Type of graph to generate"
    )
    parser.add_argument("--nodes", type = int, default = 100, help = "Number of nodes in graph")
    parser.add_argument("--tails", type = int, default = 2, help = "Number of tails conneted to graph")
    parser.add_argument("--additional_tail_nodes", type = int, default = 2, help = "Number of nodes in tail part of graph")
    parser.add_argument("--height", type = int, default = 3, help = "Height of graph (for graph types where relevant)")
    parser.add_argument("--width", type = int, default = 3, help = "Width of the graph (for graph types where relevant)")
    parser.add_argument("--seed", type = int, default = 1, help = "Seed info")
    parser.add_argument("--edges", type = int, default =10, help = "Number of edges")
    parser.add_argument("--edge_probabilty", type = float, default = 0.5, help = "Edge creation probability")
    parser.add_argument("--output", type = str, default = "edges.csv", help = "Name of output file")
    parser.add_argument("--beta", type = float, default = 0.4, help = "Model parameter")
    parser.add_argument("--alpha", type = float, default = 0.1, help = "Model parameter")

    args = parser.parse_args()
    graph_type = args.type
    graph_nodes = args.nodes
    graph_tails = args.tails
    graph_additional_tail_nodes = args.additional_tail_nodes
    graph_width = args.width
    graph_height = args.height
    graph_alpha = args.alpha
    graph_beta = args.beta
    graph_seed = args.seed

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
    elif graph_type == "random-waxman":
        graph = gen_graph_random_waxman(
            nodes = graph_nodes, 
            beta = graph_beta, 
            alpha = graph_alpha, 
            seed = args.seed)
        print(graph)
    elif graph_type == "random-geometric":
        graph = gen_graph_random_geometric(nodes = graph_nodes)
        print(graph)
    elif graph_type == "edge-swapping":
        graph = gen_graph_edge_swapping(nodes = graph_nodes)
        print(graph)
    elif graph_type == "star":
        graph = gen_graph_star(nodes = graph_nodes)
        print(graph)
    else:
        print("Unrecognized graph type!")
        exit(-1)

    write_undirected_graph_to_edges_csv(args.output, graph)

if __name__ == '__main__':
    main()