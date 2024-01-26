'''
Aggregate data
'''

import argparse
import os
import sys
import pathlib

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
    out_content = ",".join(header) + "\n"
    out_content += "\n".join(lines)

    with open(output_path, "w") as fp:
        fp.write(out_content)

    return header

def append_csv(output_path, out_lines, field_order):
    lines = []
    for info in out_lines:
        line = ",".join([str(info[field]) for field in field_order])
        lines.append(line)
    out_content = "\n" + "\n".join(lines)
    with open(output_path, "a") as fp:
        fp.write(out_content)

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

    pwip_world_summary_header = None
    pwip_world_summary_fpath = os.path.join(dump_dir, "world_summary.csv")

    incomplete_runs = []

    # Loop over runs, aggregating data from each.
    total_runs = len(run_dirs)
    cur_run_i = 0
    for run_dir in run_dirs:
        run_path = os.path.join(data_dir, run_dir)
        shared_summary_info = {}                   # Hold summary information about run. Indexed by field.
        # time_series_info =

        cur_run_i += 1
        print(f"Processing ({cur_run_i}/{total_runs}): {run_path}")

        # Skip over (but make note of) incomplete runs.
        required_files = [
            os.path.join("output", "world_summary_pwip_pa.csv"),
            os.path.join("output", "run_config.csv"),
            os.path.join("cmd.log")
        ]
        incomplete = any([not os.path.exists(os.path.join(run_path, req)) for req in required_files])
        if incomplete:
            print("  - Failed to find all required files!")
            incomplete_runs.append(run_dir)
            continue
        output_dir = os.path.join(run_path, "output")

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

        # Pull interaction matrix type from interaction matrix file
        # Expected format: {INTERACTION_MATRIX_TYPE}.dat
        interaction_matrix = os.path.split(
            cmd_params["INTERACTION_SOURCE"]
        )[1]
        interaction_matrix = interaction_matrix.split(".")[0]
        shared_summary_info["interaction_matrix_full"] = interaction_matrix

        shared_summary_info["interaction_matrix"] = "_".join(interaction_matrix.split("_")[:-1])

        print("Run configuration:", shared_summary_info)
        ############################################################

        ############################################################
        # Extract raw recorded communities
        # Identify recorded communities file to use
        fname = utils.identify_file(output_dir, "recorded_communities_raw")
        run_data_path = os.path.join(output_dir, fname)
        run_data = utils.read_csv(run_data_path)

        for line in run_data:
            raw_community_summary_content_lines.append(line)
            for field in shared_summary_info:
                raw_community_summary_content_lines[-1][field] = shared_summary_info[field]
        ############################################################

        ############################################################
        # Extract pwip recorded communities
        fname = utils.identify_file(output_dir, "recorded_communities_pwip_pa")
        run_data_path = os.path.join(output_dir, fname)
        run_data = utils.read_csv(run_data_path)

        for line in run_data:
            pwip_community_summary_content_lines.append(line)
            for field in shared_summary_info:
                pwip_community_summary_content_lines[-1][field] = shared_summary_info[field]
        ############################################################

        ############################################################
        # Extract pwip world summary (includes data over time)
        run_data_path = os.path.join(run_path, "output", "world_summary_pwip_pa.csv")
        run_data = utils.read_csv(run_data_path)

        pwip_world_summary_content_lines = []
        for line in run_data:
            pwip_world_summary_content_lines.append(line)
            for field in shared_summary_info:
                pwip_world_summary_content_lines[-1][field] = shared_summary_info[field]
        if pwip_world_summary_header == None:
            pwip_world_summary_header = write_csv(pwip_world_summary_fpath, pwip_world_summary_content_lines)
        else:
            append_csv(pwip_world_summary_fpath, pwip_world_summary_content_lines, pwip_world_summary_header)

    if len(pwip_community_summary_content_lines) > 0:
        write_csv(
            os.path.join(dump_dir, "pwip_communities_pa.csv"),
            pwip_community_summary_content_lines
        )

    if len(raw_community_summary_content_lines) > 0:
        write_csv(
            os.path.join(dump_dir, "raw_communities.csv"),
            raw_community_summary_content_lines
        )

    # Write out incomplete runs, sort them!
    incomplete_runs.sort()
    with open(os.path.join(dump_dir, "incomplete_runs_agg.log"), "w") as fp:
        fp.write("\n".join(incomplete_runs))

if __name__ == "__main__":
    main()


