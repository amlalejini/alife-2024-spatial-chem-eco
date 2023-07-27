# Experiments

This directory contains the configuration and analysis files for our experiments.
Much of the infrastructure included here for running the experiments assumes the architecture of Michigan State University's HPC.

## Steps for running an experiment on the HPC

Before running, make sure that you have the `chemical-ecology.cfg`, all graph files, and any other run configuration files necessary inside the `hpc/config/` directory (inside the experiment directory).

- Log on to the HPC and compile the chemical ecology software.
  - You will probably need to load a more recent version of GCC (e.g., `GCCcore/11.2.0`)
- Copy the executable into `hpc/config` of the experiment you're running
- Configure the `job-gen.sh` script for your account
- Run the `job-gen.sh` script to generate (1) graph files and (2) job submission scripts
- Submit the job submission scripts generated in the previous step (remember your queue limit!)