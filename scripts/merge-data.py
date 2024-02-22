'''
Merge summary data with graph properties data
'''
import argparse
import os
import utilities as utils

# columns

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

def main():
    parser = argparse.ArgumentParser(
        usage = "Merges summary data file with graph properties data file. Generates wide-format output (i.e., adds an extra column for each property)."
    )
    parser.add_argument("--graph_properties", type = str, help = "File that contains graph properties.")
    parser.add_argument("--summary_data", type = str, help = "File with summary data to append graph properties to.")
    parser.add_argument("--output_name", type = str, default = None, help = "Name of output file.")

    args = parser.parse_args()
    graph_properties_fpath = args.graph_properties
    summary_data_fpath = args.summary_data
    output_fname = args.output_name

    # Verify that input files exist.
    if not os.path.isfile(graph_properties_fpath):
        print(f"Unable to find graph properties file, {graph_properties_fpath}")
        exit(-1)
    if not os.path.isfile(summary_data_fpath):
        print(f"Unable to find summary data path, {summary_data_fpath}")
        exit(-1)

    # Read graph properties file
    graph_properties_data = utils.read_csv(graph_properties_fpath)
    # Check that graph names are unique per-row
    graph_names = {row["graph_name"] for row in graph_properties_data}
    if len(graph_names) != len(graph_properties_data):
        print("Graph names in graph properties file are not unique per-row.")
        exit(-1)
    # Key graph properties off of "graph name" attribute
    graph_properties = {row["graph_name"]:row for row in graph_properties_data}

    # Read summary data
    summary_data = utils.read_csv(summary_data_fpath)
    for row in summary_data:
        row_graph_path = row["DIFFUSION_SPATIAL_STRUCTURE_FILE"]
        graph_name = os.path.basename(row_graph_path)
        # Check that graph name exists in graph properties.
        if not graph_name in graph_properties:
            print(f"Failed to find {graph_name} from summary data in graph properties file.")
            exit(-1)
        # Append graph properties to summary data row
        for prop in graph_properties:
            row[f"grap_prop_{prop}"] = graph_properties[prop]

    summary_fname = os.path.basename(summary_data_fpath)
    summary_fname = os.path.splitext(summary_fname)[0]
    summary_path = os.path.split(summary_data_fpath)[0]
    default_out_name = os.path.join(summary_path, f"{summary_fname}_with-graph-props.csv")
    output_fname = output_fname if not output_fname is None else default_out_name
    write_csv(output_fname, summary_data)


if __name__ == "__main__":
    main()