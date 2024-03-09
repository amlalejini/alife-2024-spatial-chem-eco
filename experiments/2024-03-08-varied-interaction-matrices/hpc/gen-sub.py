'''
Generate slurm job submission scripts - one per condition
'''

import argparse, os, sys, pathlib
from pyvarco import CombinationCollector

# Add scripts directory to path, import utilities from scripts directory.
sys.path.append(
    os.path.join(
        pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parents[2],
        "scripts"
    )
)
import utilities as utils

# Configure default values for submission script
default_seed_offset = 1000
default_account = "devolab"
default_num_replicates = 30
default_job_time_request = "48:00:00"
default_job_mem_request = "4G"
default_total_updates = 300000

job_name = "02-29"
executable = "chemical-ecology"

base_script_filename = "./base_slurm_script.txt"

# Create combo object to collect all conditions we'll run
combos = CombinationCollector()
fixed_parameters = {
    "UPDATES": "20000",
    "MAX_POP": "10000",
    "V": "0",
    "DIFFUSION": "0.05",
    "SEEDING_PROB": "0.05",
    "PROB_CLEAR": "0.0",
    "REPRO_DILUTION": "0.1",
    "INTERACTION_MAGNITUDE": "1.0",
    "PROB_INTERACTION": "0.1",
    "GROUP_REPRO_SPATIAL_STRUCTURE": "load",
    "DIFFUSION_SPATIAL_STRUCTURE": "load",
    "DIFFUSION_SPATIAL_STRUCTURE_LOAD_MODE": "matrix",
    "GROUP_REPRO_SPATIAL_STRUCTURE_LOAD_MODE": "matrix",
    "STOCHASTIC_ANALYSIS_REPS": "200",
    "CELL_STABILIZATION_UPDATES": "10000",
    "CELL_STABILIZATION_EPSILON": "0.001",
    "OUTPUT_RESOLUTION": "20",
    "THRESHOLD_VALUE": "10",
    "RECORD_ASSEMBLY_MODEL": "1",
    "RECORD_ADAPTIVE_MODEL": "1",
    "GROUP_REPRO": "0"
}

special_decorators = [
    "__COPY_OVER"
]

combos.register_var("DIFFUSION_SPATIAL_STRUCTURE_FILE__COPY_OVER")
combos.register_var("INTERACTION_SOURCE__COPY_OVER")

combos.add_val(
    "DIFFUSION_SPATIAL_STRUCTURE_FILE__COPY_OVER",
    [
        "-GROUP_REPRO_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-comet-kite_${SLURM_ARRAY_TASK_ID}.mat -DIFFUSION_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-comet-kite_${SLURM_ARRAY_TASK_ID}.mat",
        "-GROUP_REPRO_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-linear-chain.mat -DIFFUSION_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-linear-chain.mat",
        "-GROUP_REPRO_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-toroidal-lattice.mat -DIFFUSION_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-toroidal-lattice.mat",
        "-GROUP_REPRO_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-well-mixed.mat -DIFFUSION_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-well-mixed.mat",
        "-GROUP_REPRO_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-random-barabasi-albert_${SLURM_ARRAY_TASK_ID}.mat -DIFFUSION_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-random-barabasi-albert_${SLURM_ARRAY_TASK_ID}.mat",
        "-GROUP_REPRO_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-random-waxman_${SLURM_ARRAY_TASK_ID}.mat -DIFFUSION_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-random-waxman_${SLURM_ARRAY_TASK_ID}.mat",
        "-GROUP_REPRO_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-cycle.mat -DIFFUSION_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-cycle.mat",
        "-GROUP_REPRO_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-wheel.mat -DIFFUSION_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-wheel.mat",
        "-GROUP_REPRO_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-star.mat -DIFFUSION_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-star.mat",
        "-GROUP_REPRO_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-windmill.mat -DIFFUSION_SPATIAL_STRUCTURE_FILE ${CONFIG_DIR}/spatial-structures/graph-windmill.mat"
    ]
)
combos.add_val(
   "INTERACTION_SOURCE__COPY_OVER",
   [
    "-N_TYPES 10 -INTERACTION_SOURCE ${CONFIG_DIR}/interaction-matrices/c25pip25.dat",
    "-N_TYPES 10 -INTERACTION_SOURCE ${CONFIG_DIR}/interaction-matrices/c25pip50.dat",
    "-N_TYPES 10 -INTERACTION_SOURCE ${CONFIG_DIR}/interaction-matrices/c25pip75.dat",
    "-N_TYPES 10 -INTERACTION_SOURCE ${CONFIG_DIR}/interaction-matrices/c50pip25.dat",
    "-N_TYPES 10 -INTERACTION_SOURCE ${CONFIG_DIR}/interaction-matrices/c50pip50.dat",
    "-N_TYPES 10 -INTERACTION_SOURCE ${CONFIG_DIR}/interaction-matrices/c50pip75.dat",
    "-N_TYPES 10 -INTERACTION_SOURCE ${CONFIG_DIR}/interaction-matrices/c75pip25.dat",
    "-N_TYPES 10 -INTERACTION_SOURCE ${CONFIG_DIR}/interaction-matrices/c75pip50.dat",
    "-N_TYPES 10 -INTERACTION_SOURCE ${CONFIG_DIR}/interaction-matrices/c75pip75.dat",
    "-N_TYPES 9 -INTERACTION_SOURCE ${CONFIG_DIR}/interaction-matrices/orig-pof.dat"
   ]
)

def main():
    parser = argparse.ArgumentParser(description="Run submission script.")
    parser.add_argument("--data_dir", type=str, help="Where is the output directory for phase one of each run?")
    parser.add_argument("--config_dir", type=str, help="Where is the configuration directory for experiment?")
    parser.add_argument("--repo_dir", type=str, help="Where is the repository for this experiment?")
    parser.add_argument("--job_dir", type=str, default=None, help="Where to output these job files? If none, put in 'jobs' directory inside of the data_dir")
    parser.add_argument("--replicates", type=int, default=default_num_replicates, help="How many replicates should we run of each condition?")
    parser.add_argument("--seed_offset", type=int, default=default_seed_offset, help="Value to offset random number seeds by")
    parser.add_argument("--account", type=str, default=default_account, help="Value to use for the slurm ACCOUNT")
    parser.add_argument("--time_request", type=str, default=default_job_time_request, help="How long to request for each job on hpc?")
    parser.add_argument("--mem", type=str, default=default_job_mem_request, help="How much memory to request for each job?")
    parser.add_argument("--runs_per_subdir", type=int, default=-1, help="How many replicates to clump into job subdirectories")

    # Load in command line arguments
    args = parser.parse_args()
    data_dir = args.data_dir
    config_dir = args.config_dir
    job_dir = args.job_dir
    repo_dir = args.repo_dir
    num_replicates = args.replicates
    hpc_account = args.account
    seed_offset = args.seed_offset
    job_time_request = args.time_request
    job_memory_request = args.mem
    runs_per_subdir = args.runs_per_subdir

    # Load in the base slurm file
    base_sub_script = ""
    with open(base_script_filename, 'r') as fp:
        base_sub_script = fp.read()

    # Get list of all combinations to run
    combo_list = combos.get_combos()

    # Calculate how many jobs we have, and what the last id will be
    num_jobs = num_replicates * len(combo_list)

    # Echo chosen options
    print(f'Generating {num_jobs} across {len(combo_list)} files!')
    print(f' - Data directory: {data_dir}')
    print(f' - Config directory: {config_dir}')
    print(f' - Repository directory: {repo_dir}')
    print(f' - Job directory: {job_dir}')
    print(f' - Replicates: {num_replicates}')
    print(f' - Account: {hpc_account}')
    print(f' - Time Request: {job_time_request}')
    print(f' - Memory: {job_memory_request}')
    print(f' - Seed offset: {seed_offset}')

    # If no job_dir provided, default to data_dir/jobs
    if job_dir == None:
        job_dir = os.path.join(data_dir, "jobs")

    # Create job file for each condition
    cur_job_id = 0
    cond_i = 0
    cur_subdir_run_cnt = 0
    cur_run_subdir_id = 0
    # generated_files = set()
    # Create a SLURM script for each treatment.
    for condition_dict in combo_list:
        cur_seed = seed_offset + (cur_job_id * num_replicates)
        filename_prefix = f'RUN_C{cond_i}'
        file_str = base_sub_script
        file_str = file_str.replace("<<TIME_REQUEST>>", job_time_request)
        file_str = file_str.replace("<<MEMORY_REQUEST>>", job_memory_request)
        file_str = file_str.replace("<<JOB_NAME>>", job_name)
        file_str = file_str.replace("<<CONFIG_DIR>>", config_dir)
        file_str = file_str.replace("<<REPO_DIR>>", repo_dir)
        file_str = file_str.replace("<<EXEC>>", executable)
        file_str = file_str.replace("<<JOB_SEED_OFFSET>>", str(cur_seed))
        file_str = file_str.replace("<<ACCOUNT_NAME>>", hpc_account)

        ###################################################################
        # Configure the run
        ###################################################################
        file_str = file_str.replace("<<RUN_DIR>>", \
            os.path.join(data_dir, f'{filename_prefix}_'+'${SEED}'))

        # Format commandline arguments for the run
        run_param_info = {key:condition_dict[key] for key in condition_dict if not any([dec in key for dec in special_decorators])}
        # Add fixed paramters
        for param in fixed_parameters:
            if param in run_param_info: continue
            run_param_info[param] = fixed_parameters[param]
        # Set random number seed
        run_param_info["SEED"] = '${SEED}'

        ###################################################################
        # Build commandline parameters string
        ###################################################################
        fields = list(run_param_info.keys())
        fields.sort()
        set_params = [f"-{field} {run_param_info[field]}" for field in fields]
        copy_params = [condition_dict[key] for key in condition_dict if "__COPY_OVER" in key]
        run_params = " ".join(set_params + copy_params)
        ###################################################################

        # Add run commands to run the experiment
        cfg_run_commands = ''
        # Set the run
        cfg_run_commands += f'RUN_PARAMS="{run_params}"\n'

        # By default, add all commands to submission file.
        array_id_run_info = {
            array_id: {
                "experiment": True
            }
            for array_id in range(1, num_replicates+1)
        }
        array_id_to_seed = {array_id:(cur_seed + (array_id - 1)) for array_id in array_id_run_info}

        # Run experiment executable
        run_commands = ''
        run_commands += 'echo "./${EXEC} ${RUN_PARAMS}" > cmd.log\n'
        run_commands += './${EXEC} ${RUN_PARAMS} > run.log\n'

        array_id_range_param = f"1-{num_replicates}"

        # -- add run commands to file str --
        file_str = file_str.replace("<<ARRAY_ID_RANGE>>", array_id_range_param)
        file_str = file_str.replace("<<CFG_RUN_COMMANDS>>", cfg_run_commands)
        file_str = file_str.replace("<<RUN_COMMANDS>>", run_commands)

        ###################################################################
        # Write job submission file (if any of the array ids are active)
        ###################################################################
        cur_job_dir = job_dir if args.runs_per_subdir == -1 else os.path.join(job_dir, f"job-set-{cur_run_subdir_id}")

        utils.mkdir_p(cur_job_dir)
        with open(os.path.join(cur_job_dir, f'{filename_prefix}.sb'), 'w') as fp:
            fp.write(file_str)

        # Update condition id and current job id
        cur_job_id += 1
        cond_i += 1
        cur_subdir_run_cnt += num_replicates
        if cur_subdir_run_cnt > (runs_per_subdir - num_replicates):
            cur_subdir_run_cnt = 0
            cur_run_subdir_id += 1

if __name__ == "__main__":
    main()
