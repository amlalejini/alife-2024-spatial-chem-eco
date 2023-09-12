#!/usr/bin/env bash

REPLICATES=20
EXP_SLUG=2023-09-12-bigger-world
ACCOUNT=devolab
SEED_OFFSET=5000
JOB_TIME=4:00:00
JOB_MEM=8G
PROJECT_NAME=artificial-ecology-spatial

GRAPH_OUTPUT_MODE=matrix

REPO_DIR=/Users/lalejina/devo_ws/${PROJECT_NAME}
HOME_EXP_DIR=${REPO_DIR}/experiments/${EXP_SLUG}

DATA_DIR=${HOME_EXP_DIR}/hpc/test
JOB_DIR=${HOME_EXP_DIR}/hpc/test
CONFIG_DIR=${HOME_EXP_DIR}/hpc/config

# Activate appropriate python virtual environment
source ${REPO_DIR}/pyenv/bin/activate
# Generate graphs
python3 gen-graphs.py --dump_dir ${CONFIG_DIR}/spatial-structures --base_seed ${SEED_OFFSET} --replicates ${REPLICATES} --output_mode ${GRAPH_OUTPUT_MODE}
# Generate job submission scripts
python3 gen-sub.py --time_request ${JOB_TIME} --mem ${JOB_MEM} --data_dir ${DATA_DIR} --config_dir ${CONFIG_DIR} --repo_dir ${REPO_DIR} --replicates ${REPLICATES} --job_dir ${JOB_DIR} --account ${ACCOUNT} --seed_offset ${SEED_OFFSET}