#!/bin/bash
# Single-GPU job inside the Apptainer image.
#   sbatch slurm/gpu_job.sbatch scripts/wandb_smoke.py [args...]
#
# Lines marked SITE must be set to this cluster's values (see `sinfo`).
#SBATCH --job-name=fm-gpu
#SBATCH --partition=gpu            # SITE
#SBATCH --gres=gpu:1               # SITE
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

set -euo pipefail

REPO=${REPO:-$SLURM_SUBMIT_DIR}
IMAGE=${IMAGE:-$REPO/env/cryoet-fm.sif}
DATA=${DATA:-$REPO/data}

cd "$REPO"
mkdir -p logs "$DATA"

echo "job $SLURM_JOB_ID on $(hostname) | $(date)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true

apptainer exec --nv \
    --bind "$REPO":"$REPO" --bind "$DATA":"$DATA" \
    --pwd "$REPO" \
    "$IMAGE" python "$@"
