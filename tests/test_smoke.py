import dtwin
from dtwin.utils import config, io, log, run, seed  # noqa: F401  (import check)


def test_version():
    assert dtwin.__version__
