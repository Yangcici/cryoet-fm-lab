"""Smoke test: confirm the GPU is visible and that a run reaches Weights & Biases.

Usage:
    uv run python scripts/wandb_smoke.py                 # logs online
    WANDB_MODE=offline uv run python scripts/wandb_smoke.py   # no account needed
"""

import platform
import time

import torch
import wandb


def main() -> None:
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else device

    run = wandb.init(
        project="cryoet-fm-lab",
        job_type="smoke-test",
        config={
            "torch": torch.__version__,
            "device": device,
            "gpu": gpu_name,
            "n_gpus": torch.cuda.device_count(),
            "host": platform.node(),
        },
    )
    print(f"torch {torch.__version__} | device {device} | gpu {gpu_name}")

    # Tiny regression so the loss curve proves that training and logging both work.
    torch.manual_seed(0)
    x = torch.randn(4096, 16, device=device)
    y = x @ torch.randn(16, 1, device=device)
    model = torch.nn.Linear(16, 1).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)

    start = time.time()
    for step in range(200):
        loss = torch.nn.functional.mse_loss(model(x), y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 10 == 0:
            wandb.log({"loss": loss.item()}, step=step)
    print(f"final loss {loss.item():.5f} in {time.time() - start:.1f}s")
    run.finish()


if __name__ == "__main__":
    main()
