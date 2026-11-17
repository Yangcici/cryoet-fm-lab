"""Download N tomograms from one CryoET Data Portal dataset and write a manifest.

One tomogram is taken per run (runs sorted by name, so the selection is
reproducible). Files already on disk with the right size are skipped, so the
script can be re-run after an interruption.

Usage:
    uv run python scripts/pull_tomograms.py --dry-run
    uv run python scripts/pull_tomograms.py --dataset 10003 --n 20 --out data/tomograms
"""

import argparse
import csv
import hashlib
from pathlib import Path

import mrcfile
from cryoet_data_portal import Client, Run, TiltSeries, Tomogram

MANIFEST_FIELDS = [
    "dataset_id", "run_id", "run_name", "tomogram_id", "voxel_spacing_A",
    "size_x", "size_y", "size_z", "reconstruction_method", "processing",
    "tilt_min", "tilt_max", "tilt_step", "bytes", "sha256", "file", "source_url",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 24), b""):
            digest.update(block)
    return digest.hexdigest()


def select(client: Client, dataset_id: int, n: int, processing: str | None) -> list[dict]:
    """Pick one tomogram from each of the first n runs that have one."""
    tilts = {
        ts.run_id: ts
        for ts in TiltSeries.find(client, [TiltSeries.run.dataset_id == dataset_id])
    }
    by_run: dict[int, list[Tomogram]] = {}
    for tomo in Tomogram.find(client, [Tomogram.run.dataset_id == dataset_id]):
        if processing and tomo.processing != processing:
            continue
        by_run.setdefault(tomo.run_id, []).append(tomo)

    rows = []
    runs = sorted(Run.find(client, [Run.dataset_id == dataset_id]), key=lambda r: r.name)
    for run in runs:
        candidates = sorted(by_run.get(run.id, []), key=lambda t: t.id)
        if not candidates:
            continue
        tomo = candidates[0]
        ts = tilts.get(run.id)
        rows.append({
            "dataset_id": dataset_id,
            "run_id": run.id,
            "run_name": run.name,
            "tomogram_id": tomo.id,
            "voxel_spacing_A": tomo.voxel_spacing,
            "size_x": tomo.size_x,
            "size_y": tomo.size_y,
            "size_z": tomo.size_z,
            "reconstruction_method": tomo.reconstruction_method,
            "processing": tomo.processing,
            "tilt_min": ts.tilt_min if ts else "",
            "tilt_max": ts.tilt_max if ts else "",
            "tilt_step": ts.tilt_step if ts else "",
            "bytes": tomo.file_size_mrc,
            "source_url": tomo.https_mrc_file,
            "_tomo": tomo,
        })
        if len(rows) == n:
            break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dataset", type=int, default=10003, help="portal dataset id")
    parser.add_argument("--n", type=int, default=20, help="number of tomograms")
    parser.add_argument("--out", type=Path, default=Path("data/tomograms"))
    parser.add_argument("--processing", default=None,
                        help="keep only this processing type (raw, denoised, filtered)")
    parser.add_argument("--dry-run", action="store_true", help="list the selection, download nothing")
    args = parser.parse_args()

    rows = select(Client(), args.dataset, args.n, args.processing)
    total_gb = sum(r["bytes"] or 0 for r in rows) / 1e9
    print(f"dataset {args.dataset}: {len(rows)} tomograms selected, {total_gb:.1f} GB")
    if len(rows) < args.n:
        print(f"warning: only {len(rows)} of the requested {args.n} are available")

    if args.dry_run:
        for r in rows:
            print(f"  run {r['run_name']:<24} tomo {r['tomogram_id']}  "
                  f"{r['size_x']}x{r['size_y']}x{r['size_z']} @ {r['voxel_spacing_A']} A  "
                  f"{(r['bytes'] or 0) / 1e9:.2f} GB  {r['processing']}")
        return

    out = args.out / str(args.dataset)
    out.mkdir(parents=True, exist_ok=True)
    for i, r in enumerate(rows, 1):
        tomo = r.pop("_tomo")
        dest = out / f"{r['run_name']}_{r['tomogram_id']}.mrc"
        if dest.exists() and dest.stat().st_size == r["bytes"]:
            print(f"[{i}/{len(rows)}] have {dest.name}")
        else:
            print(f"[{i}/{len(rows)}] downloading {dest.name}")
            tomo.download_mrcfile(dest_path=str(out))
            Path(out / Path(r["source_url"]).name).rename(dest)

        # Open the header to prove the file is a readable volume of the expected shape.
        with mrcfile.mmap(dest, permissive=True) as mrc:
            shape = (int(mrc.header.nx), int(mrc.header.ny), int(mrc.header.nz))
        expected = (r["size_x"], r["size_y"], r["size_z"])
        if shape != expected:
            raise SystemExit(f"{dest.name}: shape {shape} does not match portal {expected}")
        r["sha256"] = sha256(dest)
        r["file"] = dest.name

    with (out / "manifest.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {out / 'manifest.csv'} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
