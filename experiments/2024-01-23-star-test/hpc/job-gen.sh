#!/usr/bin/env bash

REPLICATES=20
EXP_SLUG=2024-01-23-star-test
ACCOUNT=devolab
SEED_OFFSET=1000
JOB_TIME=01:00:00
JOB_MEM=8G
PROJECT_NAME=artificial-ecology

GRAPH_OUTPUT_MODE=matrix

SCRATCH_EXP_DIR=/mnt/scratch/sheajoh2/data/${PROJECT_NAME}
REPO_DIR=/mnt/home/sheajoh2/devo_ws/${PROJECT_NAME}
HOME_EXP_DIR=${REPO_DIR}/experiments

DATA_DIR=${SCRATCH_EXP_DIR}/${EXP_SLUG}
JOB_DIR=${SCRATCH_EXP_DIR}/${EXP_SLUG}/jobs
CONFIG_DIR=${HOME_EXP_DIR}/${EXP_SLUG}/hpc/config

# Activate appropriate python virtual environment
source ${REPO_DIR}/pyenv/bin/activate
# Generate graphs
python3 gen-graphs.py --dump_dir ${CONFIG_DIR}/spatial-structures --base_seed ${SEED_OFFSET} --replicates ${REPLICATES} --output_mode ${GRAPH_OUTPUT_MODE}
# Generate job submission scripts
python3 gen-sub.py --time_request ${JOB_TIME} --mem ${JOB_MEM} --data_dir ${DATA_DIR} --config_dir ${CONFIG_DIR} --repo_dir ${REPO_DIR} --replicates ${REPLICATES} --job_dir ${JOB_DIR} --account ${ACCOUNT} --seed_offset ${SEED_OFFSET}