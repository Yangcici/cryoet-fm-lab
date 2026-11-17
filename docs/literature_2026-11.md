# Literature check, November 2026: generative restoration in cryo-ET

Scan date 2026-11-17. Scope: diffusion, score-based and flow-matching methods for denoising or missing-wedge restoration in cryo-ET published after February 2026, plus the nearest non-generative methods and benchmarks.

"Opened" means the abstract or full text was read. "Snippet" means only a search summary was seen.

## Generative methods on cryo-ET data

| Work | Date | Method | Real data | Code | Read |
|---|---|---|---|---|---|
| [CryoET-DDM](https://doi.org/10.1093/bioinformatics/btag824) (Wang … Wan, Bioinformatics) | 2026-11-12 | Diffusion denoising of 2D tilt series, with background-noise patches from the same series in the forward process | EMPIAR-10499, 10164, 10651; scored by subtomogram averaging | [repo](https://github.com/wxinsheng/CryoET-DDM), no licence | Abstract only |
| [MW-RaMViD](https://www.biorxiv.org/content/10.64898/2026.02.15.706025v1.full) (Hasan … Jonic, bioRxiv) | 2026-02-17 | Video diffusion that generates the unacquired high-tilt images before reconstruction | None, synthetic tilt series only | Not found | Full text |

## Non-generative methods to compare against

| Work | Date | Method | Code |
|---|---|---|---|
| [IsoNet2](https://www.biorxiv.org/content/10.64898/2025.12.09.693325v1) (Liu … Zhou, bioRxiv) | 2025-12-11; v2.1.0 released 2026-10-29 | End-to-end self-supervised missing-wedge filling with built-in Noise2Noise, network-based CTF correction and per-tomogram wedge geometry | [repo](https://github.com/IsoNet-cryoET/IsoNet2), GPL-3.0, no general pretrained weights |
| [ICECREAM](https://journals.iucr.org/d/issues/2026/04/00/zi5009/index.html) (Kishore … Dokmanić, Acta Cryst. D) | 2026-03-27 | Self-supervised equivariant imaging plus Noise2Noise | [repo](https://github.com/swing-research/icecream) |
| [cryoDeRec](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_A_Supervised_Multi-task_Framework_for_Joint_cryo-ET_Restoration_Enabled_by_CVPR_2026_paper.html) (Wang … Hu, CVPR 2026) | 2026 | Supervised joint denoising and wedge recovery trained on simulated pairs | Repo seen in a snippet only |

## Evaluation and benchmarks

- [Jones, Deshmukh and Pande](https://journals.iucr.org/d/issues/2026/03/00/sor5005/) (Acta Cryst. D, 2026-02-19): systematic comparison of existing restoration methods by downstream template matching, subtomogram averaging and segmentation on four experimental datasets. Abstract only.
- [CAHRA](https://heterogeneity.notion.site/challenge) is a single-particle cryo-EM heterogeneity challenge (closed June 2026), not a cryo-ET one. Its metrics (minimum-RMSD structure accuracy, RMSF difference, proportion of captured variance) do not apply to tomogram restoration.

## Generative priors with hard data consistency, outside cryo-ET

- [NSIRE](https://doi.org/10.1038/s41467-026-74189-4) (Nature Communications, 2026-06-16): diffusion prior with null-space iterations for atomic electron tomography of nanoparticles.
- [LUCID](https://arxiv.org/abs/2609.10456) (arXiv, 2026-09-09): multi-view diffusion priors with projection-domain consistency for the X-ray laminography missing cone.
- [TEMDiff](https://arxiv.org/abs/2510.06516) (arXiv, 2025-10-07): 3D diffusion prior with projector guidance for limited-angle TEM, simulated results only.
- [CryoLVM](https://arxiv.org/abs/2602.02620) (arXiv, 2026-02-02): JEPA foundation model on cryo-EM density maps; missing-wedge restoration is one downstream task, on maps rather than tomograms.

## Gaps in this scan

- bioRxiv was read through its API and Europe PMC, which can lag by a few weeks, so October–November 2026 preprints may be missing.
- arXiv coverage rests on web search and keyword sweeps; OpenReview was not searched.
- Not found: any flow-matching method for cryo-ET tomograms, or 3D diffusion posterior sampling on experimental tomograms.

## Reading order

1. IsoNet2 preprint and repository.
2. Jones, Deshmukh and Pande, then CryoET-DDM for how a diffusion method was validated on EMPIAR data.
