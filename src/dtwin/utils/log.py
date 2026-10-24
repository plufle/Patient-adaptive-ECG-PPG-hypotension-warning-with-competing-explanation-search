"""Consistent logging to the console and, optionally, a run's log file.

(Named ``log`` rather than ``logging`` to avoid shadowing the standard library.)
"""

from __future__ import annotations

import logging
from pathlib import Path

_FORMAT = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str = "dtwin", log_file: str | Path | None = None, level: int = logging.INFO) -> logging.Logger:
    """Return a logger with one console handler, plus a file handler if ``log_file`` is given.

    Safe to call repeatedly (e.g., re-running a notebook cell): handlers are not duplicated.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False
    formatter = logging.Formatter(_FORMAT, _DATEFMT)

    if not any(type(h) is logging.StreamHandler for h in logger.handlers):
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    if log_file is not None:
        log_file = Path(log_file).resolve()
        has_file = any(
            isinstance(h, logging.FileHandler) and Path(h.baseFilename) == log_file for h in logger.handlers
        )
        if not has_file:
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(formatter)
            logger.addHandler(fh)
    return logger
