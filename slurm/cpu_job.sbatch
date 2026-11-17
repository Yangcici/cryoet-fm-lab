#!/bin/bash
# CPU-only job inside the Apptainer image (downloads, preprocessing).
#   sbatch slurm/cpu_job.sbatch scripts/pull_tomograms.py --out data/tomograms
#
# Lines marked SITE must be set to this cluster's values (see `sinfo`).
#SBATCH --job-name=fm-cpu
#SBATCH --partition=cpu            # SITE
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=12:00:00
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

set -euo pipefail

REPO=${REPO:-$SLURM_SUBMIT_DIR}
IMAGE=${IMAGE:-$REPO/env/cryoet-fm.sif}
DATA=${DATA:-$REPO/data}

cd "$REPO"
mkdir -p logs "$DATA"

echo "job $SLURM_JOB_ID on $(hostname) | $(date)"

apptainer exec \
    --bind "$REPO":"$REPO" --bind "$DATA":"$DATA" \
    --pwd "$REPO" \
    "$IMAGE" python "$@"
