#!/bin/bash
# Array of single-GPU jobs, one per line of a parameter file (seeds, ablations).
#   sbatch --array=1-3 slurm/array_job.sbatch scripts/train.py params.txt
# Line N of params.txt holds the extra arguments for array task N.
#
# Lines marked SITE must be set to this cluster's values (see `sinfo`).
#SBATCH --job-name=fm-array
#SBATCH --partition=gpu            # SITE
#SBATCH --gres=gpu:1               # SITE
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=08:00:00
#SBATCH --output=logs/%x-%A_%a.out
#SBATCH --error=logs/%x-%A_%a.err

set -euo pipefail

SCRIPT=$1
PARAMS=$2

REPO=${REPO:-$SLURM_SUBMIT_DIR}
IMAGE=${IMAGE:-$REPO/env/cryoet-fm.sif}
DATA=${DATA:-$REPO/data}

cd "$REPO"
mkdir -p logs "$DATA"

ARGS=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$PARAMS")
echo "job ${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID} on $(hostname) | args: $ARGS"

# shellcheck disable=SC2086  # word splitting of $ARGS is intended
apptainer exec --nv \
    --bind "$REPO":"$REPO" --bind "$DATA":"$DATA" \
    --pwd "$REPO" \
    "$IMAGE" python "$SCRIPT" $ARGS
