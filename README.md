# cryoet-fm-lab

A learning log for flow matching and diffusion models applied to cryo-electron tomography (cryo-ET). Small, runnable experiments, each with the command that reproduces it.

## Setup

```bash
uv sync                                   # local environment from uv.lock
uv run python scripts/wandb_smoke.py      # checks torch, the GPU and W&B logging
```

On a Slurm cluster, the same locked environment runs inside an Apptainer image:

```bash
apptainer build env/cryoet-fm.sif env/cryoet-fm.def
sbatch slurm/gpu_job.sbatch scripts/wandb_smoke.py
```

Set the lines marked `SITE` in `slurm/*.sbatch` to your cluster's partition and GPU flags first.

## Data

Tomograms come from the [CryoET Data Portal](https://cryoetdataportal.czscience.com). Nothing is stored in this repo.

```bash
uv run python scripts/pull_tomograms.py --dry-run                 # list the selection
sbatch slurm/cpu_job.sbatch scripts/pull_tomograms.py --out data/tomograms
```

The default is 20 raw tomograms from dataset 10003 (*M. pneumoniae* 70S ribosomes, ±60° tilt, 6.8 Å voxels, about 31 GB). The script writes `manifest.csv` with portal IDs, shapes, tilt range and checksums.

## Layout

| Path | What it holds |
|---|---|
| `env/cryoet-fm.def` | Apptainer definition: CUDA base image plus the locked uv environment |
| `slurm/` | Job templates: single GPU, CPU-only, and GPU array |
| `scripts/wandb_smoke.py` | Environment smoke test |
| `scripts/pull_tomograms.py` | Reproducible tomogram download with a manifest |
| `docs/` | Reading notes and literature checks |

## Log

- **Week 1:** environment, job templates, data download script.
