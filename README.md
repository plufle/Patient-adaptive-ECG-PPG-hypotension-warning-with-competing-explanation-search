# Patient-adaptive ECG–PPG hypotension warning with competing-explanation search

Research code for a retrospective study. The system:

- warns of intraoperative hypotension from ECG and PPG, adapted to each patient;
- explains a detected change physiologically **only when the signals can tell the candidate explanations apart**. It does this by explicitly searching for competing explanations (physiological or sensor-related) that fit the same signals.

> Status: early development (phase P0, foundations). There are no results yet. This is research code, not a medical device.

The full research protocol and implementation plan is in [CLAUDE.md](CLAUDE.md).

## Setup

**Local (CPU)**

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows; on Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"         # add extras as needed: sim, signal, ml (or all)
pytest
```

**Google Colab**

Open [notebooks/00_setup_colab.ipynb](notebooks/00_setup_colab.ipynb) on a Colab runtime and run all cells. The notebook mounts Google Drive, where data and runs are stored under `MyDrive/dtwin/`, clones this repository and runs the tests.

## Layout

| Path | Contents |
|---|---|
| `src/dtwin/` | Package code. All logic lives here |
| `configs/` | YAML configs. `base.yaml` holds every provisional setting |
| `notebooks/` | Thin Colab notebooks that call the package |
| `tests/` | `pytest` suite |
| `data/`, `runs/` | Local data and run outputs (gitignored; on Colab they live on Drive) |

## Data

Raw patient data and derived data are **never** committed. Datasets such as VitalDB and MIMIC must be obtained from their providers under their own licences and terms.
