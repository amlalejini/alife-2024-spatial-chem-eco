'''
Aggregate data
'''

import argparse, os, sys, pathlib
sys.path.append(
    os.path.join(
        pathlib.Path(
            os.path.dirname(os.path.abspath(__file__))).parents[2],
            "scripts"
    )
)
import utilities as utils

run_identifier = "RUN_"

run_cfg_fields = [
    "CELL_STABILIZATION_EPSILON",
    "OUTPUT_RESOLUTION",
    "CELL_STABILIZATION_UPDATES",
    "GROUP_REPRO_SPATIAL_STRUCTURE",
    "PROB_INTERACTION",
    "DIFFUSION_SPATIAL_STRUCTURE",
    "N_TYPES",
    "UPDATES",
    "MAX_POP",
    "DIFFUSION_SPATIAL_STRUCTURE_FILE",
    "STOCHASTIC_ANALYSIS_REPS",
    "DIFFUSION",
    "INTERACTION_SOURCE",
    "DIFFUSION_SPATIAL_STRUCTURE_LOAD_MODE",
    "SEED",
    "SEEDING_PROB",
    "REPRO_DILUTION",
    "PROB_CLEAR",
    "GROUP_REPRO_SPATIAL_STRUCTURE_FILE",
    "GROUP_REPRO_SPATIAL_STRUCTURE_LOAD_MODE",
    "INTERACTION_MAGNITUDE",
    "world_size"
]

def write_csv(output_path, summary_dict):
    # (1) What's the header?
    header = list(summary_dict[0].keys())
    header.sort()
    # (2) Collect all lines as strings
    lines = []
    for info in summary_dict:
        line_header_info = sorted(list(info.keys()))
        if line_header_info != header:
            print("Header mismatch!")
            exit(-1)
        line = ",".join([str(info[field]) for field in header])
        lines.append(line)
    out_content = "\n".join(lines)

    with open(output_path, "w") as fp:
        fp.write(out_content)

# TODO:
# - Extract and output world_summary_pwip information (in addition to recorded community info already being output)
# - Test script on John's data

def main():
    parser = argparse.ArgumentParser(description="Run submission script.")
    parser.add_argument("--data_dir", type=str, help="Where is the base output directory for each run?")
    parser.add_argument("--dump", type=str, help="Where to dump this?", default=".")

    # Parse command line arguments
    args = parser.parse_args()
    data_dir = args.data_dir
    dump_dir = args.dump

    # Verify that the given data directory exits
    if not os.path.exists(data_dir):
        print("Unable to find data directory.")
        exit(-1)

    # Create the directory to dump aggregated data (if it doesn't already exist)
    utils.mkdir_p(dump_dir)

    # Aggregate run directories.
    run_dirs = [run_dir for run_dir in os.listdir(data_dir) if run_identifier in run_dir]
    print(f"Found {len(run_dirs)} run directories.")

    # Create data structure to hold summary information for each run (1 element per run)
    # Aggregates from "recorded_communities_raw.csv"
    raw_community_summary_content_lines = []
    # Aggregates from "recorded_communities_pwip.csv"
    pwip_community_summary_content_lines = []
    # Aggregates from "world_summary_pwip.csv"
    pwip_world_summary_content_lines = []

    incomplete_runs = []

    # Loop over runs, aggregating data from each.
    total_runs = len(run_dirs)
    cur_run_i = 0
    for run_dir in run_dirs:
        run_path = os.path.join(data_dir, run_dir)
        shared_summary_info = {}                   # Hold summary information about run. Indexed by field.

        cur_run_i += 1
        print(f"Processing ({cur_run_i}/{total_runs}): {run_path}")

        # Skip over (but make note of) incomplete runs.
        required_files = [
            os.path.join("output", "recorded_communities_pwip.csv"),
            os.path.join("output", "recorded_communities_raw.csv"),
            os.path.join("output", "run_config.csv"),
            os.path.join("cmd.log")
        ]
        incomplete = any([not os.path.exists(os.path.join(run_path, req)) for req in required_files])
        if incomplete:
            print("  - Failed to find all required files!")
            incomplete_runs.append(run_dir)
            continue

        ############################################################
        # Extract configs from run_config.csv file
        cfg_path = os.path.join(run_path, "output", "run_config.csv")
        cfg_data = utils.read_csv(cfg_path)
        cmd_params = {}
        for line in cfg_data:
            param = line["parameter"]
            value = line["value"]
            cmd_params[param] = value
            if param in run_cfg_fields:
                shared_summary_info[param] = value

        # Pull graph type from graph file name.
        # Expected format: graph-{GRAPH_TYPE}_{REPID}.csv
        graph_type = os.path.split(
            cmd_params["DIFFUSION_SPATIAL_STRUCTURE_FILE"]
        )[1]
        graph_type = graph_type.replace("graph-", "")
        graph_type = graph_type.split(".")[0]
        graph_type = graph_type.split("_")[0]
        shared_summary_info["graph_type"] = graph_type
        print("Run configuration:", shared_summary_info)
        ############################################################

        ############################################################
        # Extract raw recorded communities
        run_data_path = os.path.join(run_path, "output", "recorded_communities_raw.csv")
        run_data = utils.read_csv(run_data_path)

        for line in run_data:
            raw_community_summary_content_lines.append(line)
            for field in shared_summary_info:
                raw_community_summary_content_lines[-1][field] = shared_summary_info[field]
        ############################################################

        ############################################################
        # Extract pwip recorded communities
        run_data_path = os.path.join(run_path, "output", "recorded_communities_pwip.csv")
        run_data = utils.read_csv(run_data_path)

        for line in run_data:
            pwip_community_summary_content_lines.append(line)
            for field in shared_summary_info:
                pwip_community_summary_content_lines[-1][field] = shared_summary_info[field]
        ############################################################

        ############################################################
        # Extract pwip recorded communities
        run_data_path = os.path.join(run_path, "output", "world_summary_pwip.csv")
        run_data = utils.read_csv(run_data_path)

        for line in run_data:
            pwip_world_summary_content_lines.append(line)
            for field in shared_summary_info:
                pwip_world_summary_content_lines[-1][field] = shared_summary_info[field]
        ############################################################

    write_csv(
        os.path.join(dump_dir, "pwip_communities.csv"),
        pwip_community_summary_content_lines
    )

    write_csv(
        os.path.join(dump_dir, "raw_communities.csv"),
        raw_community_summary_content_lines
    )

    write_csv(
        os.path.join(dump_dir, "world_summary.csv"),
        pwip_world_summary_content_lines
    )

    # Write out incomplete runs, sort them!
    incomplete_runs.sort()
    with open(os.path.join(dump_dir, "incomplete_runs_agg.log"), "w") as fp:
        fp.write("\n".join(incomplete_runs))

if __name__ == "__main__":
    main()


