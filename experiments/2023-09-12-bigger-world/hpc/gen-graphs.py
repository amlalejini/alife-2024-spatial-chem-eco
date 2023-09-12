import argparse
import os
import sys
import pathlib
import copy
import inspect

# Add scripts directory to path, import utilities from scripts directory.
sys.path.append(
    os.path.join(
        pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parents[2],
        "scripts"
    )
)
import SpatialStructure as structs
import utilities as utils

graphs = {
    "well-mixed": {
        "graph": "well-mixed",
        "args": {"nodes": 1024},
        "shared": True
    },
    "toroidal-lattice": {
        "graph": "toroidal-lattice",
        "args": {"graph_height": 32, "graph_width": 32},
        "shared": True
    },
    "comet-kite": {
        "graph": "comet-kite",
        "args": {"core_size": 408, "num_tails": 208, "additional_tail_nodes": 408},
        "shared": False
    },
    "linear-chain": {
        "graph": "linear-chain",
        "args": {"nodes": 1024},
        "shared": True
    },
    "random-barabasi-albert": {
        "graph": "random-barabasi-albert",
        "args": {"nodes": 1024, "edges": 102},
        "shared": False
    },
    "random-waxman": {
        "graph": "random-waxman",
        "args": {"nodes": 1024, "beta": 0.4, "alpha": 0.2},
        "shared": False
    }
}

generators = {
    "well-mixed": structs.gen_graph_well_mixed,
    "toroidal-lattice": structs.gen_graph_toroidal_lattice,
    "comet-kite": structs.gen_graph_comet_kite,
    "circular-chain": structs.gen_graph_circular_chain,
    "linear-chain": structs.gen_graph_linear_chain,
    "star": structs.gen_graph_star,
    "random-erdos-renyi": structs.gen_graph_random_erdos_renyi,
    "random-barabasi-albert": structs.gen_graph_random_barabasi_albert,
    "random-waxman": structs.gen_graph_random_waxman,
    "random-geometric": structs.gen_graph_random_geometric
}

def main():
    parser = argparse.ArgumentParser(description="Run submission script.")
    parser.add_argument("--base_seed", type=int, default=2, help="Random number seed to use for any graphs that require a seed")
    parser.add_argument("--replicates", type=int, default=10, help="How many replicates should we run of each condition?")
    parser.add_argument("--output_mode", type=str, default="matrix", choices=["matrix", "edges"], help="What format should graphs be written?")
    parser.add_argument("--dump_dir", type=str, default=".", help="Where to dump files?")

    args = parser.parse_args()

    write_fun = None
    output_extension = ""
    if args.output_mode == "edges":
        write_fun = structs.write_undirected_graph_to_edges_csv
        output_extension = "csv"
    else:
        write_fun = structs.write_undirected_graph_to_matrix
        output_extension = "mat"

    output_extension = "csv" if args.output_mode == "edges" else "mat"
    seed = args.base_seed
    generated_graphs = {}
    for graph_id in graphs:
        print(f"Generating {graph_id}")
        info = graphs[graph_id]
        graph_generator = generators[info["graph"]]
        graph_args = copy.copy(info["args"]) # Make a copy of arguments that we may modify
        generator_arguments = inspect.getfullargspec(graph_generator).args

        if info["shared"]:
            # Generate a single graph for all replicates
            out_name = f"graph-{graph_id}.{output_extension}"

            if ("seed" in generator_arguments) and ("seed" not in graph_args):
                graph_args["seed"] = seed
                seed += 1

            generated_graphs[out_name] = {
                "graph": graph_generator(**graph_args),
                "file": out_name,
                "seed": None if "seed" not in graph_args else graph_args["seed"]
            }
        else:
            # Generate a unique graph for each replicate
            for array_id in range(1, args.replicates+1):
                # Count by slurm array ids (which use 1-indexing)
                out_name = f"graph-{graph_id}_{array_id}.{output_extension}"

                if "seed" in generator_arguments:
                    graph_args["seed"] = seed
                    seed += 1

                generated_graphs[out_name] = {
                    "graph": graph_generator(**graph_args),
                    "file": out_name,
                    "seed": None if "seed" not in graph_args else graph_args["seed"]
                }

    # Write out graph files
    utils.mkdir_p(args.dump_dir)
    for graph in generated_graphs:
        info = generated_graphs[graph]
        write_fun(
            fname = os.path.join(args.dump_dir, info["file"]),
            graph = info["graph"]
        )

    print("-- Files written: --")
    print("\n".join(f"{g}: {generated_graphs[g]}" for g in generated_graphs))


if __name__ == "__main__":
    main()