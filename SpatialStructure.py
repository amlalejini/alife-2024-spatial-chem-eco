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

def gen_graph_toroidal_lattice():
    pass

def gen_graph_comet_kite():
    pass

def gen_graph_circular_chain():
    pass

def gen_graph_linear_chain():
    pass

def gen_graph_random_blah():
    pass

def gen_graph_random_blah2():
    pass

def main():
    parser = argparse.ArgumentParser(
        usage="Program for generating graphs"
    )
    parser.add_argument("--type", type = str, default = "well-mixed", choices = ["well-mixed"], help = "Type of graph to generate")
    parser.add_argument("--nodes", type = int, default = 10, help = "Number of nodes in graph")

    args = parser.parse_args()
    graph_type = args.type
    graph_nodes = args.nodes

    graph = None
    if graph_type == "well-mixed":
        graph = gen_graph_well_mixed(nodes = graph_nodes)
        print(graph)
    else:
        print("Unrecognized graph type!")
        exit(-1)




if __name__ == '__main__':
    main()