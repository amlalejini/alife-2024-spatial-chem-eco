import argparse
import os
import networkx as nx
import matplotlib.pyplot as plt
import utilities as utils
import numpy as np
import graph_utilities as graph_utils
# import nxviz as nv

def main():
    parser = argparse.ArgumentParser(
        usage = "Merges summary data file with graph properties data file. Generates wide-format output (i.e., adds an extra column for each property)."
    )
    parser.add_argument("--graph_dir", type = str, help = "Directory containing graphs to visualize")
    parser.add_argument("--graph_file_identifiers", type = str, nargs="+", default=["graph"], help = "Set of strings to match to in graph file names.")
    parser.add_argument("--dump_dir", type = str, default = "./", help = "Where to write output files?")

    args = parser.parse_args()
    graph_dir = args.graph_dir
    graph_file_identifiers = args.graph_file_identifiers
    dump_dir = args.dump_dir

    utils.mkdir_p(dump_dir)

    # Verify that the given graph directory exits
    if not os.path.exists(graph_dir):
        print("Unable to find graph directory.")
        exit(-1)
    # Gather file names of graphs to process
    graph_files = [f for f in os.listdir(graph_dir) if all([s in f for s in graph_file_identifiers])]
    cur_g = 0
    for graph_file in graph_files:
        cur_g += 1
        print(f"-- {graph_file} --")
        print(f"Processing graph {cur_g} / {len(graph_files)}")
        graph_path = os.path.join(graph_dir, graph_file)
        # Load graph from file
        graph = graph_utils.read_graph_matrix(graph_path, directed=False)
        # Draw
        # pos = nx.spring_layout(
        #     graph,
        #     scale = 50
        # )
        # d = dict(graph.degree)
        # nx.draw_networkx(
        #     graph,
        #     pos,
        #     node_color = 'lightblue',
        #     with_labels = True
        # )
        pos = nx.layout.spectral_layout(
            graph,
            scale = 2
        )
        pos = nx.spring_layout(
            graph,
            pos=pos,
            k = 5 / np.sqrt(graph.order())
        )
        fig = plt.figure(figsize=(16, 16))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        nx.draw_networkx(
            graph,
            pos,
            linewidths=1
        )
        # Output graph
        graph_name = os.path.basename(graph_file)
        output_path = os.path.join(dump_dir, f"{graph_name}.png")
        plt.savefig(
            output_path,

        )
        plt.close()

if __name__ == "__main__":
    main()
