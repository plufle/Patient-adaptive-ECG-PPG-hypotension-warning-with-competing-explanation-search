"""One place to seed every random number generator the project uses."""

from __future__ import annotations

import os
import random

import numpy as np


def set_seed(seed: int, deterministic_torch: bool = False) -> np.random.Generator:
    """Seed Python, NumPy and (if installed) PyTorch; return a NumPy Generator.

    Prefer passing the returned Generator around over using global NumPy state.

    Args:
        seed: the seed.
        deterministic_torch: also request deterministic PyTorch kernels (slower on GPU).
    """
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)  # only affects child processes
    try:
        import torch
    except ImportError:
        pass
    else:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        if deterministic_torch:
            torch.use_deterministic_algorithms(True, warn_only=True)
            torch.backends.cudnn.benchmark = False
    return np.random.default_rng(seed)
