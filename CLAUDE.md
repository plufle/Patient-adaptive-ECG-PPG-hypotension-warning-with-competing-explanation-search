# CLAUDE.md — Patient-Adaptive Hybrid ECG–PPG Monitoring (Cardiovascular Digital-Twin Programme)

This file is the working specification for the project: the aim, the scientific protocol, the implementation design, the experiments and the conventions. Read it fully before making changes.

**Document history**
- **v2 (2026-10-24):** revised according to the external scientific review [RESEARCH_PLAN_REVIEW_2026-10-24.md](RESEARCH_PLAN_REVIEW_2026-10-24.md).
- **v1:** archived in [docs/archive/CLAUDE_v1_2026-10-24.md](docs/archive/CLAUDE_v1_2026-10-24.md).

**Adoption status.** On **2026-10-24 the owner adopted v2.1**, including all of v2. Tags such as **[PROPOSED]** now only mark where an item came from (a review). Values marked [PROVISIONAL] are still open until G-LOCK. Numbers marked **[PROVISIONAL]** are research operating points. They are not clinical acceptability claims and must be frozen before final testing (§7.6).

---

## 1. Vision, first-study aim and claims

### 1.1 Long-term vision (unchanged; not the claim of the first paper)

> An interpretable cardiovascular digital-twin system that continuously integrates multimodal data — ECG, PPG, wearable sensors, imaging and clinical measurements — to distinguish normal patient-specific variability from clinically meaningful abnormalities, identify the likely physiological source, and give early warnings with quantified uncertainty.

### 1.2 First-study aim [PROPOSED]

> To develop and retrospectively validate a patient-adaptive ECG–PPG model for early warning of intraoperative hypotension, and to quantify when the available signals support a physiological explanation of the detected change.

### 1.3 Candidate contribution [PROPOSED — v2.1]

**Main idea:** turn physiological ambiguity into something the model explicitly tests, learns from and reports.

**Main method: Competing-Explanation Search (CES)** (§4.9). For every alert, the system:
1. fits the explanation the model supports;
2. actively searches for the strongest *different* explanation — physiological **or sensor-related** — that reproduces the same observed history;
3. tests, with a simulation-calibrated test, whether the signals distinguish the two;
4. reports the supported explanation, the strongest competitor, the evidence gap between them, and **"unresolved"** when they cannot be distinguished.

**Training component: Ambiguity-Aware Training (AAT)** (§4.5). Deliberately ambiguous examples are used *in training*, not only in evaluation. The model thereby learns not to discriminate confidently between mechanisms that the observation model cannot separate.

> **Proposed research question:** Can a patient-adaptive ECG–PPG warning system reduce incorrect physiological explanations, by explicitly searching for competing mechanisms that fit the observed signals, while preserving useful hypotension warning performance?

**Claim boundaries**
- **Relation to existing methods:** CES is related to profile likelihood and generalized likelihood-ratio testing, which are established. The contribution must show a **distinct procedure** or a **practical advantage** over them at matched explanation availability (E6). The distinct procedure has four parts:
  - explanation-level hypotheses that include sensor-change alternatives;
  - sequential operation over the history with warm starts;
  - simulation-calibrated rejection;
  - the explicit competing fit returned as evidence.
- **If CES does not beat those comparators:** report the work as a *validated monitoring framework and benchmark*. Do not claim algorithmic novelty.
- **Not novel by itself:** the four-component combination ("patient-specific + hybrid + multimodal + uncertainty"), abstention or rejection of uncertain measurements, personalized test-time adaptation for hypotension, and robust ECG–PPG fusion all already appear in prior work (§1.5).
- **No clinical causes:** clinical cause claims stay limited (§4.9, level L3).

### 1.3a Alternative contributions (retained; not the main line)

| ID | Idea | Why it is not the main line | Cheap part kept in the main plan |
|---|---|---|---|
| **A3** | **Anchored adaptation:** personalize the reference without absorbing slow deterioration. Keep an initial patient anchor, and adapt only to supported changes in acquisition conditions | Must beat existing adaptation methods (e.g., CSA-TTA). Benign drift and deterioration are not always separable from ECG–PPG | Fixed-anchor deviation is always reported (§4.6); E4 includes a gradual-decline subgroup |
| **A4** | **Decision-relevant measurement selection:** decide when an extra measurement (e.g., a cuff BP) would change the warning or the explanation | Larger extension; changes the inference setting; revealing ABP values is an *idealized* measurement experiment, not validated cuff operation | None (future work) |

- **For a method contribution:** the explanation rule (§4.9) must be defined mathematically and compared with ordinary posterior-uncertainty thresholding and with existing hybrid inference.
- **If the final method is only a combination of existing components:** describe the contribution as a *validated monitoring framework and benchmark*. Do not claim algorithmic novelty.
- **Not novel by itself:** the four-component combination ("patient-specific + hybrid + multimodal + uncertainty") and abstention or rejection of uncertain measurements both already appear in prior work (§1.5).

### 1.4 Terminology rules

| Use | Avoid (until justified) |
|---|---|
| "Patient-adaptive hybrid monitoring model" | "Digital twin" for the first-study system |
| "Individual reference state", "patient-specific perioperative baseline" | "Normal physiology" (intraoperative data cannot establish everyday normal physiology) |
| "Pulse arrival time (PAT)", for ECG R-peak to PPG foot | "PTT" for the same quantity (PAT includes the pre-ejection period, PEP) |
| "Model-compatible explanation", "unresolved" | Clinical causes ("hypovolemia", "reduced contractility") without independent validation |
| "Warning ≥ 10 min before onset" (matched-interval definition, §3.4) | "10 minutes early" when the label is "event within 10 min" |

"Retrospective hemodynamic digital-twin prototype" may be used only after patient-specific state updating **and** posterior predictive checks have been demonstrated.

### 1.5 Closest prior work (from the review; **links not yet verified by Claude** — check each before citing)

| Work | Overlap | Implication |
|---|---|---|
| Wehenkel et al., *Simulation-based Inference for Cardiovascular Models* (arXiv 2307.13918, 2023/2024) | Cardiovascular neural posterior estimation, uncertainty, ambiguous solutions | SBI, posterior uncertainty and observed non-identifiability are established ingredients |
| Manduchi et al., *Leveraging Cardiovascular Simulations for In-Vivo Prediction of Cardiac Biomarkers* (arXiv 2412.17542, 2024) | Hemodynamic SBI, simulated PPG, VitalDB evaluation, hybrid learning, uncertainty-based rejection | Strong overlap with the inference plan. Some of its real-data results use arterial-pressure inputs, so do not describe them as ECG–PPG-only |
| Zhang et al., *PMB-NN* (CMPB 2026; arXiv 2512.10745) | Personalized PPG monitoring with Windkessel constraints and neural networks; notes R/C identifiability limits | Personalized hybrid PPG physiology is not new by itself. Compare online updating and warning behaviour directly |
| Park et al., *SNUPHY-M* (arXiv 2509.08830, 2025) | ECG/PPG/ABP pretraining; noninvasive hypotension prediction on VitalDB at 5/10/15 min | Multimodality and these horizons are established. Include it as a representation-learning comparator if reproducible (code: github.com/Vitallab-AI/SNUPHY-M) |
| Tong et al., *InVAErt networks* (arXiv 2408.08264, 2025) | Amortized inverse modelling and non-identifiability analysis in lumped models | "Identifiability-aware" alone is not a novelty claim. A new decision rule, evaluation or demonstrated benefit is needed |
| Thiel et al., WCCM–ECCOMAS 2026 abstract | Bayesian 0D hypotension modelling, sequential updating | Sequential updating is being studied. This is an abstract without real-patient validation |
| Cardiovascular mechanistic-modelling guidelines (PMC11442102) | Recommends establishing identifiability and not interpreting non-unique estimates biologically | Governs §4.4 |
| *CSA-TTA* (arXiv 2512.15762) | Personalized test-time adaptation for hypotension prediction | Adaptation (RQ1) is not novel by itself. Use it as an E4 comparator if reproducible |
| *CardioFusion-AI* (arXiv 2608.26000) | Robust ECG–PPG fusion | Fusion (RQ3) is not novel by itself. Cite it, and compare where possible |
| *Embed and Emulate* (arXiv 2409.18402) | Generic contrastive learning for non-identifiable simulation problems | AAT must be distinguished by its mechanism-specific ambiguity objective and its measured effect on explanation errors |
| Profile likelihood / likelihood-ratio identifiability methods (established) | Distinguishing parameter values from data | The CES comparator in E6. CES must show a distinct procedure or a practical advantage |

**M0 deliverable:** a contribution-by-contribution comparison table in `paper/related_work.md`. That review was targeted, not systematic.

---

## 2. Research questions and hypotheses [PROPOSED]

**Primary question — explanation (v2.1).** Does Competing-Explanation Search reduce incorrect confident physiological explanations at **matched explanation availability**, compared with posterior-threshold, uncertainty-threshold and profile-likelihood rules, on an independent benchmark (RQ4)?

**Co-primary requirement — warning.** In held-out adult surgical patients, the patient-adaptive ECG–PPG system that carries CES must preserve **event-level hypotension warning sensitivity** at a pre-specified false-alarm burden.
- It is compared with **equally personalized** data-driven models.
- The test is non-inferiority with a margin fixed at G-LOCK [PROVISIONAL]. Superiority is tested as RQ2.

"Equally personalized" is essential. Beating a fixed population threshold would not show that the mechanistic component adds value.

| RQ | Hypothesis | Required evidence |
|---|---|---|
| **RQ1:** Does adaptation help? | Past-only patient adaptation improves event sensitivity at the chosen alarm budget, compared with the same model with adaptation disabled | Paired continuous replay; identical eligibility and alert policies; patient-clustered CIs; comparison with existing test-time adaptation (CSA-TTA) if reproducible |
| **RQ2:** Does physiology add useful information? | A reduced hybrid model improves warning sensitivity or risk calibration over a personalized data-driven model with the same inputs, history, supervision and tuning effort | Physics-only, data-only, hybrid, and hybrid-without-residual comparisons. Parameter count is secondary |
| **RQ3:** When does ECG add value to PPG? | Fusion improves warning performance under pre-specified conditions, and the gain changes when timing information is removed or corrupted | Matched modality ablations; PAT-removal ablation; timing-jitter tests; monitoring-availability reporting. **Do not assume PAT dominates** |
| **RQ4:** Does an explicit competitor search make explanations more reliable? | CES has lower selective explanation error than the posterior-mass rule, posterior-SD thresholding, profile-likelihood intervals and a selective data-driven classifier **at the same explanation availability**, under noise, sensor changes, ambiguous and combined causes, unknown scenarios and model mismatch | Independent benchmark (§7.3); risk–coverage curves; real-data attribution only where independent references exist |
| **RQ5:** Does training on ambiguity help? | With the architecture fixed, AAT reduces confident errors between indistinguishable mechanisms without losing distinguishable detections, on an independent simulator and on unseen sensor distortions | E6b: ordinary training vs AAT. The baseline **must** include NPE trained with the full nuisance model |

**There are three separate uncertainty and calibration claims.** Do not merge them into one "90% coverage" hypothesis.

| Claim | What it means | How it is evaluated |
|---|---|---|
| U1 | Parameter-posterior calibration | Simulation only: coverage, contraction, SBC, prior and mismatch sensitivity. This does not establish real physiological coverage |
| U2 | Event-risk calibration | Held-out Brier score, reliability curves, calibration slope and intercept, discrimination. ECE is supplementary, with its binning stated |
| U3 | Alarm performance | False alert episodes per eligible monitoring hour, event sensitivity, precision, alert duration and lead time, in continuous replay |

---

## 3. Data

### 3.1 Datasets and their roles

| Dataset | Role in the first study | Access (verify and pin the exact release) | Notes |
|---|---|---|---|
| **VitalDB** | **Primary** development and internal test; raw continuous replay | Open; `pip install vitaldb` | 6,388 operations from 6,090 subjects (dataset paper). **Split by `subjectid`** |
| **PulseDB v2_0** | Optional pretraining | Open (github.com/pulselabteam/PulseDB) | v2_0 adds timestamps and non-normalized fields. Patient provenance must be resolved against the VitalDB and MIMIC test sets (§3.5). Its MIMIC-III part has inter-signal misalignment of up to 500 ms; prefer the VitalDB-derived part for timing work |
| **MIMIC-III Waveform Matched Subset v1.0 / MIMIC-IV Waveform v0.1.0** | External test, gated on synchronization (§3.6) | Waveforms are listed as open under their licences; linked EHR access is separate. Pin the release | Apply for EHR credentials only if EHR variables are actually needed |
| **PPG-DaLiA** | Secondary robustness test: motion, signal quality, timing, observation availability | Open (UCI) | **No** BP-event or mechanism targets. Never report hypotension accuracy from it. Sessions are too short for a "first-day" baseline |
| PTB-XL, MIT-BIH, LTAF | **Deferred** (arrhythmia work for a later study) | Open (PhysioNet) | They do not validate multimodal physiology in this cohort |

**Primary endpoint:** hypotension only. AF, hypertension, ischemia and general "cardiac abnormality" detection are deferred to later studies.

**Ambulatory or wearable warning claims:** these need a separate, endpoint-appropriate dataset or study. They are not part of the first paper.

### 3.2 VitalDB specifics

- Access: `vitaldb.find_cases([...])`, `vitaldb.load_case(caseid, track_names, interval)`, plus the clinical table, which contains `subjectid`.
- Tracks of interest (**verify names against the track list**):
  - `SNUADC/ECG_II`, `SNUADC/PLETH` and `SNUADC/ART` (native rate ~500 Hz);
  - `Solar8000/ART_MBP` (numeric);
  - any cardiac-output or SV monitor tracks, for the independent-reference audit (§3.7).
- Initial inclusion criteria:
  - adult;
  - ECG_II, PLETH and ART all present;
  - at least 60 min of overlapping signal.
- **Audit, rather than silently apply,** any exclusion that could depend on disease severity (§4.1).

### 3.3 Inference setting [PROPOSED]

| Setting | Inputs at inference | Role |
|---|---|---|
| **Main** | ECG + PPG + static pre-op variables | Primary claims |
| Cuff-calibrated (optional, named separately) | Main + initial cuff BP | Secondary. A cuff reading still does **not** resolve the SV/R/C scaling symmetry (§4.4) |
| ABP oracle (optional, labelled) | Main + continuous ABP | Upper-bound benchmark only. Never used to claim ECG–PPG superiority |

ABP is used **only** for training targets and retrospective outcome adjudication.

### 3.4 Event and warning definitions [PROPOSED — clinician review required before freezing]

**Hypotension event**
- Definition: MAP < 65 mmHg sustained for at least 60 s, from ABP after artifact handling.
- ABP artifact handling: detect flush and square-wave segments, zeroing and calibration segments, damping and line occlusion. Rules live in `configs/events.yaml`. Audit every rule on the pilot.
- Gaps: an event cannot be confirmed across an ABP gap longer than `gap_max_s` (provisional 10 s). Windows whose label depends on such a gap are **censored**, not negative.
- Event end (recovery): MAP ≥ 65 mmHg sustained for at least `recovery_s` (provisional 60 s).
- Merging: events separated by less than `merge_s` (provisional 60 s) are merged. Recurrent events are kept and counted, and patient-level event counts are reported.

**Censoring**
- Prediction times without enough future observation (end of record, long gaps) are excluded as **censored**, never labelled negative.

**Eligibility**
- A prediction time is eligible when:
  - ECG/PPG observation rules pass (§4.1);
  - the patient is not currently in an event;
  - the patient is not within `post_event_refractory_s` after an event ends (provisional 10 min);
  - the future label is not censored.
- Always report the eligible fraction of total recorded time.

**Three tasks — keep them distinct**

| Task | Target at time t |
|---|---|
| T-detect (present event) | Is the patient in an event now? Secondary task only |
| T-predict-h (horizon) | Onset in (t, t + h], with h ∈ {5, 10, 15} min. Used for training and as a secondary analysis |
| **T-warn (primary)** | **Onset in [t + 10, t + 15] min.** This is the matched interval for the "≥ 10 min warning" claim [PROVISIONAL] |

If the pilot supports only a shorter lead time, **revise the protocol before final testing**. Do not relabel the results afterwards.

**Alert episodes and matching**
- The alert policy has three parameters, all frozen before testing (§7.6):
  - persistence: the risk score must stay above the threshold for `persist_s`;
  - merging of nearby episodes;
  - a refractory period of `refractory_s` after an alert.
- An event counts as **warned (≥ 10 min)** if an alert episode starts 10–15 min before its onset.
- A **false alert episode** is an episode with no event onset within (0, 15] min of its start and that does not start during an ongoing event. [PROVISIONAL; clinician review]

**Treatment context**
- Vasopressor and fluid records are reported as context only.
- Associations with treatment are not interpreted as treatment effects, and treatment is not used as a definitive cause label.

### 3.5 Splits and leakage control [PROPOSED]

- **Group by `subjectid`, not `caseid`.** All operations from one person go to the same split.
- **Four roles:**
  - train;
  - tune (model selection);
  - **calibration** (threshold and alert-policy selection, recalibration);
  - test (final, touched once).
- Suggested starting ratio: 60 / 10 / 10 / 20 by subject. Cross-fitting within train + tune is allowed.
- Split files are saved to `data/splits/*.json` with the seed. Never regenerate them silently.
- **Pretraining provenance:** before any PulseDB pretraining, map PulseDB segments to their source subjects and drop every subject that appears in the VitalDB tune, calibration or test splits or in the MIMIC external test. Unsupervised pretraining does **not** remove this concern.
- **Static variables:** only those available at prediction time (age, sex, height, weight, BMI, ASA, pre-op labs or diagnoses). No whole-operation drug totals, outcomes or post-op tests.
- **Causality:** filters, resampling, imputation, feature extraction, normalization and baseline updates must use only data up to the alert time. Use causal filters, or report the buffering delay and include it in the lead time.

### 3.6 External validation gate (MIMIC)

- Check ECG–PPG synchronization **per source and per record** before using a record for PAT-dependent models.
- Successful cross-correlation alignment does **not** recover true PAT, because it can remove the physiological delay.
- Records failing the synchronization check are evaluated with a **timing-agnostic variant** only, and the transportability claim is limited accordingly.
- Report results by source and by synchronization eligibility.

### 3.7 Independent physiological references

- ABP gives pressure-event labels and waveform references. It is **not** independent ground truth for SV, resistance, preload or contractility.
- On the pilot, audit whether any VitalDB subset has independent CO/SV monitoring. Record the device, its measurement method and its limitations.
- A quantity computed from the same pressure model is a *model-derived* reference, not independent truth.
- Without an independent reference, physiological attribution is evaluated **in simulation only** (§7.3).

### 3.8 Inputs and storage

Signals are stored continuously, and windows are sliced on the fly. This avoids storing overlapping windows twice.

| Item | Specification |
|---|---|
| Continuous storage | Per case: ECG and PPG at 125 Hz, ABP at 125 Hz (labels and reference only), float16, plus per-sample quality masks |
| Fiducial points | Beat fiducials (R-peaks, PPG foot, systolic peak, notch) **detected at the native ~500 Hz rate** and stored as float timestamps. PAT is computed from these: one 125 Hz sample is 8 ms, too coarse. Report the timing error of the detector on synthetic signals with known delay |
| Window | 10 s (1,250 samples at 125 Hz), evaluated every 5 s |
| `x_wave` | `[2, 1250]`, ECG and PPG z-scored per window. The raw scale goes to `x_scale` as a **nuisance** variable: amplitude and DC depend on device and contact as well as physiology |
| `x_mask` | `[2, 1250]` validity mask |
| `x_feat` | Window-level features (§4.2) |
| `x_hist` | Rolling history of features and model outputs over the last `H` minutes (provisional H = 10 min). This is the input to the risk head (§4.7) |
| `x_static` | Pre-op static variables only |
| Labels | `y_abp` (SBP/DBP/MAP), `y_event_now`, `y_warn` (T-warn), `y_pred_h`, `censored`, `eligible` |
| Synthetic only | `theta_true`, `scenario_label`, `distinguishable_set` |

**Storage budget**
- About 10.8 MB per 4-hour case for three float16 channels, plus masks, fiducials and labels.
- Use the pilot to measure the real size.
- Choose the final cohort size from **event yield and precision** on the pilot, not from storage.

---

## 4. Method

### 4.1 Preprocessing and observation rules

**ECG**
- Causal band-pass 0.5–40 Hz.
- Add a mains notch only if it is justified for the data (after a 40 Hz low-pass it usually is not).
- R-peaks from two detectors, with agreement checked.

**PPG**
- Causal band-pass, e.g., 0.5–8 Hz.
- Foot via intersecting tangents; also the systolic peak.
- Dicrotic-notch detection only if its reliability is validated (§4.2).

**Signal quality**
- A template-matching SQI per channel.
- **Observation availability** (whether each modality is usable) is a first-class output and is reported separately from prediction and explanation availability.

**Audit flags, not hard rejections**
- MAP outside 40–150 mmHg.
- Disagreement between ECG HR and PPG HR.

Genuine severe events and pulse deficits can violate these checks. Report everything rejected, and analyse whether exclusions depend on disease.

**Gaps**
- No interpolation across gaps longer than 2 s; mask them instead.

### 4.2 Features

| Group | Features | Conditions |
|---|---|---|
| ECG timing | RR mean and SD, HR | — |
| HRV | RMSSD, SDNN over **rolling ≥ 60 s histories** (primary) | 10 s ultra-short variants only as separately validated secondary features |
| ECG morphology | QRS width, QT/QTc, ST-level proxy | Only after reliability checks under the chosen filtering and sampling. No diagnostic ECG interpretation is claimed |
| PPG morphology | Pulse amplitude (nuisance-scaled), rise time, width at 50% height, decay time constant, reflection index | Dicrotic-notch features only if their reliability is validated. **No "SpO2-like" features**: single-channel PPG amplitude is not SpO2. A perfusion-index proxy only if raw AC/DC access is available |
| Cross-modal | **PAT** (R-peak → PPG foot, computed at the native rate), PAT variability | PAT = PEP + vascular transit + device latency. Never interpret it as PTT or as stiffness on its own |
| Static | Age, sex, BMI, ASA, pre-op variables | Available at prediction time only |

### 4.3 Observation model (what the signals can tell the model)

The model predicts what the sensors would record. These terms link the physics model to the measured signals:

- **ECG:** gives the RR intervals (HR) and the electrical timing reference.
- **PAT:**
  PAT = PEP + PTT_vasc + δ_dev + ε.
  - PEP is the pre-ejection period, which is **unobserved**. It is a nuisance parameter with a prior.
  - δ_dev is the device and acquisition latency. Correct it only when a documented device offset exists, and **never** in a way that removes the physiological delay.
  - ε is timing noise.
- **PPG:**
  PPG(t) = g · h_τ ∗ P_ao(t − PTT_vasc) + b + noise.
  - g is an unknown gain and b an unknown offset: PPG is uncalibrated.
  - h_τ is a first-order low-pass filter.
  - This is a modelling assumption and must be stated as such in the paper.

### 4.4 Mechanistic model and identifiability gate [PROPOSED — must run before any SBI work]

**Base model: WK3**
- C · dP_p/dt = Q(t) − P_p / R_p
- P_ao = P_p + Z_c · Q(t)
- Q(t) is a half-sine ejection of stroke volume SV over ejection time T_ej, repeated every RR interval.

**Known structural symmetry**

Hold HR, T_ej and the waveform shape fixed, and pick any a > 0. Then the substitution
- SV → a·SV
- R_p → R_p / a
- C → a·C
- Z_c → Z_c / a
- Q → a·Q

leaves P_ao(t) unchanged, given the same initial pressure, and so the PPG is unchanged too.

Consequences:
- **SV, R_p, C and Z_c are not separately identifiable** from pressure *or* PPG unless something independent measures flow or volume.
- With uncalibrated PPG (unknown g and b), the absolute pressure level is not identifiable either.
- Fixing parameters removes degrees of freedom but **does not make the fixed values correct** for a patient.
- Clinical priors regularize the estimate. They are **not** observed information and must never be presented as such.

**Candidate identifiable quantities** (hypotheses to *test*, not assume):
- the time constant τ_RC = R_p · C;
- the ratio Z_c / R_p;
- T_ej / RR;
- HR;
- the total delay (PEP + PTT_vasc);
- the PPG filter τ.

Possible trade-offs to check: τ_RC against τ_filter, and PEP against PTT_vasc. PEP and PTT_vasc are expected to be **non-separable** from ECG + PPG alone.

**Gate G-ID** (results go in `runs/<id>/identifiability.md`)
1. **Structural analysis:** symmetry and scaling analysis of the full observation model (§4.3), plus a symbolic or numerical rank check of the sensitivity matrix.
2. **Practical analysis:** with noise and nuisance variables:
   - sensitivity and Fisher-information rank;
   - posterior geometry (ridges, multimodality);
   - prior sensitivity;
   - posterior predictive checks;
   - held-out recovery error.
3. **Reporting rule:** keep SBC, but **do not** treat SBC or recovered-vs-true correlation as proof of identifiability or clinical validity. Report HR separately, because a directly measured parameter must not inflate the apparent recovery success.
4. **Decision:** the reduced parameterization θ_red (the quantities that pass) is recorded in §14.
   - If no hemodynamic quantity beyond HR and PAT passes, keep warning prediction and **revise the explanation claim** (§1.3).

Escalate to a closed-loop 0D model **only** for a specific, validated need *and* with measurements that can constrain it.

**Implementation**
- PyTorch, vectorized RK4 or `torchdiffeq`, GPU-batched.
- The simulator samples nuisance variables: g, b, PEP, δ_dev, noise, baseline wander, motion artifacts.

### 4.5 Amortized inference

- **Method:** NPE with the `sbi` library over θ_red plus the nuisance variables, which are marginalized out.
- **Embedding:** a 1D-CNN over `x_wave`, concatenated with `x_feat`.
- **Training:** simulated (θ, x) pairs with realistic corruptions. Adaptation to real data must not use test or calibration subjects.
- **Multimodal posteriors:** evaluate posterior predictive simulations from **posterior samples**, not just the posterior mean (which can be implausible).

**Ambiguity-Aware Training (AAT) [PROPOSED — v2.1]**

Training data include three kinds of constructed examples. The simulator generates all of them; the classes are fixed after G-ID.

| Example | Construction | Desired behaviour |
|---|---|---|
| Sensor-only change | Same θ_red; change in PPG gain/offset, filter τ or device delay | Keep the supported physiological conclusion; represent the information that was lost |
| Indistinguishable pair | Different θ with observations matched within noise (e.g., along the WK3 scaling symmetry, or the PEP vs PTT_vasc trade-off) | Return the compatible set, or "unresolved" |
| Distinguishable change | A change in a quantity that passed G-ID | Detect and explain it |

- **Objective** (applies to the explanation head and the scenario classifier):
  - For an ambiguous example, the target is its **compatible set**: the classes whose best constrained fit lies within the noise tolerance, computed by simulation.
  - A penalty applies to probability mass that concentrates on one member of an indistinguishable set. Examples: cross-entropy to a uniform-over-set target, or a set-valued loss.
- **Expected effect:** an NPE trained by maximum likelihood on a correct simulator that already includes the nuisances should learn non-identifiability by itself. AAT's benefit is therefore expected mainly in two places:
  - discriminative explanation heads and classifiers;
  - misspecification and unseen distortions.
- **Fair comparison:** E6b must use the nuisance-complete NPE as its baseline, or the effect of AAT will be overstated.

### 4.6 Patient reference state and sequential updating [PROPOSED]

**Past-only reference rule (fixed and pre-specified)**
- Built from the first `ref_minutes` (provisional 15) of windows that pass the ECG–PPG observation rules.
- The selection uses **no ABP and no event labels**.
- Selecting a "stable period" with ABP or future labels is an **oracle** setting. It may only be reported separately, clearly labelled.

**Cold start**
- A population prior (optionally conditioned on static covariates) is used until the reference exists.
- Report cold-start performance. Never drop patients without a reference.

**Updating**
- A slow, past-only update of the reference (EMA with half-life `ref_halflife_min`, provisional 60).
- The update is frozen while the ECG–PPG-derived deviation exceeds the freeze threshold (no ABP is used).
- **Known failure mode:** a slow deterioration can be absorbed into the reference before the deviation reaches the freeze threshold.
  - **Mitigation:** always compute the deviation against the **fixed initial anchor** as well, and pass both to the risk head.
  - A dedicated anchored-adaptation rule is the alternative contribution A3 (§1.3a).

**Sequential state posterior (optional)**
- If a Bayesian filter is used, update it on **non-overlapping** 10 s windows, or model the shared data in overlapping windows. Never multiply likelihoods from overlapping windows as if they were independent.
- A per-window posterior plus an EMA is **not** a sequential state posterior and must not be called one.

### 4.7 Risk head (forecasting component) [PROPOSED]

The posterior, deviation and change-point outputs describe the **present** state. A separate risk head makes the **future-event** prediction.

- **Input:** `x_hist` over the last H minutes (the observed history), containing:
  - window features;
  - posterior summaries of θ_red (mean, SD);
  - deviation scores relative to the reference;
  - residual scores;
  - change-point statistics;
  - observation-availability flags;
  - plus `x_static`.
- **Output:** p(T-warn | history), plus T-predict-h for h = 5, 10, 15.
- **First implementation:** logistic regression or gradient boosting on summarized history. A small GRU/TCN is an alternative.
- Full mechanistic forecasting (simulating the state forward) is optional future work.
- **Recalibration:** Platt or isotonic scaling, fitted on the **calibration** subjects only.

### 4.8 Deviation, residual and change points

- **Deviation:** z_{k,t} = (θ̂_{k,t} − μ_k) / σ_k, computed against the reference spread.
- **Posterior uncertainty** s_{k,t} is reported **separately**. Folding it into the z-score would shrink the deviation, and uncertain deterioration would then look normal.
- **Three statuses kept separate:** *observation failure*, *high state uncertainty* and *normal*.
- **Residual model:** small, a conditional autoencoder on the real window vs the posterior-predictive simulation.
  - Validate that it does **not** absorb the physiological changes the mechanistic part should explain. Test this by injecting θ_red changes in simulation and checking that the residual score stays low.
- **Change points:** BOCPD on θ_red trajectories, with CUSUM as the simple baseline. Trend = slope over recent windows.

### 4.9 Explanation output (three levels) [PROPOSED]

| Level | Content | When it is shown |
|---|---|---|
| L1: observed change | What was measured, e.g. "PAT −35 ms vs reference", "PPG decay constant −20%", "HR +18 bpm" | Whenever observation is available |
| L2: model-compatible explanation | A set of θ_red changes (or scenario classes) consistent with the data, e.g. {"τ_RC ↓"} or {"τ_RC ↓", "filter τ ↓"} | Only when the **distinguishability rule** passes; otherwise **"unresolved"** |
| L3: clinical cause | e.g. vasodilation, hypovolemia | **Not in the first study** unless independently validated (§3.7). In simulation, scenario labels are used only as known interventions |

**Distinguishability rule: Competing-Explanation Search (CES) [PROPOSED — v2.1; formalize in M4]**

**Explanation classes** (`configs/explanations.yaml`, fixed after G-ID). Each class E_j is a constrained region of the (θ_red, nuisance) space, relative to the patient reference:
- physiological classes: directional changes of each θ_red quantity (e.g., τ_RC↓, τ_RC↑, total delay↑, HR↑) and pre-specified combinations;
- **sensor / acquisition classes:** PPG gain or offset change, PPG filter-τ change, device-delay change, motion artifact;
- "no change", meaning reference variability only.

**Likelihood ℓ(θ; x)**
- Default: the explicit noise model of §4.3, a Gaussian over beat-aligned features and downsampled waveforms.
- Alternative: neural likelihood estimation.
- Step 4 below calibrates the test by simulation, so the test does not rely on the independence assumptions of ℓ.

**Procedure.** Runs at every alert, and on a sparse schedule otherwise. It uses the past-only history x_{t−H_e:t} (H_e provisional 5 min).
1. **Primary fit.** For each class: θ̂_j = argmax over θ ∈ E_j of ℓ(θ; x). Warm-start from amortized NPE samples restricted to E_j, and refine by gradient through the differentiable simulator. The supported explanation Ê is the class with the highest ℓ(θ̂_j), and its fit is θ̂.
2. **Competitor.** The strongest competitor E_c is the best-fitting class other than Ê.
3. **Evidence gap.** Δ_j = ℓ(θ̂) − ℓ(θ̂_j) for each competitor.
4. **Simulation-calibrated rejection.**
   - Simulate replicate histories from θ̂_j, with nuisances sampled.
   - Recompute Δ_j on each replicate. This gives its distribution if E_j were true.
   - Reject E_j if the observed Δ_j exceeds the (1 − α_e) quantile of that distribution.
5. **Output.**
   - Every competitor rejected → **resolved: Ê**.
   - Otherwise → **unresolved**, returning Ê, the non-rejected competitors (strongest first), their gaps and their fitted trajectories as evidence.
   - If the posterior predictive check on Ê fails → **"no model-compatible explanation"** (model mismatch).
6. **Efficiency.**
   - Warm-start from previous fits.
   - Recompute only on state change or alert.
   - Use a fixed, recorded compute budget per alert, and report the runtime.

**Comparators.** All use the same classes and the same information.
- Forced choice (argmax).
- The **posterior-mass rule** (the v2 rule): report the smallest set with posterior mass ≥ 1 − α_e; single explanation only if the set has size 1 and the PPC passes.
- Posterior-SD thresholding.
- **Per-parameter profile-likelihood intervals.** The explanation is reported if the interval excludes "no change" in one direction only.
- A data-driven scenario classifier trained on the same synthetic labels, with selective abstention (max-probability or conformal sets).

**Evaluation**
- **Risk–coverage curves:** selective explanation error against explanation availability.
- **Primary summary:** selective error **at matched availability** (provisional 50% and 70%), plus AURC. Always answering "unresolved" therefore cannot win.
- **Abstaining from an explanation never suppresses a warning.** A hypotension warning may be issued with mechanism = "unresolved".

**Alert record** (JSON)
```json
{
  "subject_id": "...", "case_id": "...", "t_alert": 0, "risk": 0.0, "threshold": 0.0,
  "observation": {"ecg": "ok", "ppg": "ok"},
  "observed_changes": [{"feature": "PAT", "delta": -0.035, "unit": "s"}],
  "state": [{"param": "tau_RC", "z": -2.4, "posterior_sd": 0.3}],
  "explanation": {"status": "resolved|unresolved|no_model_compatible",
                  "supported": "tau_RC_down",
                  "strongest_competitor": "ppg_filter_change",
                  "gap": 0.0, "gap_threshold": 0.0,
                  "non_rejected": ["ppg_filter_change"]},
  "trend": [{"param": "tau_RC", "slope_per_min": -0.02}],
  "setting": "main"
}
```

---

## 5. Repository layout

```
paper/
├── CLAUDE.md
├── RESEARCH_PLAN_REVIEW_2026-10-24.md   # external review behind v2
├── docs/archive/                        # superseded plan versions
├── README.md
├── pyproject.toml                       # package "dtwin"
├── configs/                             # experiments; events.yaml; alert_policy.yaml; explanations.yaml
├── src/dtwin/
│   ├── data/          # vitaldb.py, mimic.py, pulsedb.py, dalia.py, splits.py, provenance.py
│   ├── preprocess/    # causal_filters.py, sqi.py, fiducials.py, observation.py
│   ├── labels/        # abp_artifacts.py, events.py, censoring.py, eligibility.py
│   ├── features/      # ecg.py, ppg.py, pat.py, history.py
│   ├── physics/       # windkessel.py, observation_model.py, simulator.py, scenarios.py
│   ├── identifiability/  # symmetry.py, sensitivity.py, practical.py
│   ├── inference/     # npe.py, embedding.py, residual.py, ppc.py, ambiguity_training.py (AAT)
│   ├── twin/          # reference.py, deviation.py, changepoint.py, filter.py
│   ├── risk/          # risk_head.py, recalibration.py
│   ├── explain/       # classes.py, ces.py (competing-explanation search), comparators.py, explanation.py
│   ├── alerts/        # policy.py (persistence/merge/refractory), matching.py
│   ├── baselines/     # thresholds.py, personal_features.py, gbm.py, neural.py, snuphy_m.py
│   ├── eval/          # replay.py, alarm_metrics.py, calibration.py, bootstrap.py, attribution.py
│   └── utils/         # io.py (paths), config.py, seed.py, log.py, run.py
├── notebooks/         # thin Colab notebooks, numbered by stage (00_setup_colab …)
├── scripts/           # build_dataset.py, run_identifiability.py, train_*.py, run_replay.py, run_eval.py
├── tests/
├── paper/             # manuscript, related_work.md, figures/, tables/
├── data/              # gitignored
└── runs/              # gitignored
```

---

## 6. Compute and environment

- **Runtime:** Google Colab GPU (T4), used through the Colab VS Code extension. Notebooks are edited locally and run on the Colab kernel.
- **Local files are not visible to the Colab runtime.** All paths go through `dtwin.utils.io`:
  - on Colab: `/content/drive/MyDrive/dtwin/...`;
  - locally: `./data` and `./runs`.
  - Copy data to `/content/` before heavy reads.
- **Code delivery:** the public GitHub repo (§12). `00_setup_colab.ipynb` clones or pulls it and runs `pip install -e .[extras]`. Logic lives in `src/dtwin/`.
- **Local environment:** `.venv` in the repo (gitignored). Create it with `python -m venv .venv` and `.venv\Scripts\python -m pip install -e ".[dev]"`.
- **Session limits:** checkpoint to Drive every N steps and resume automatically. Long jobs run in chunks.
- **Packages:** `numpy`, `scipy`, `pandas`/`polars`, `torch`, `torchdiffeq`, `sbi`, `neurokit2`, `vitaldb`, `wfdb`, `scikit-learn`, `lightgbm`, `matplotlib`, `pyyaml`. Pin versions once the environment works.
- **Reproducibility:** each run saves its `run_id`, resolved config, git hash, seed and split-file hashes.

---

## 7. Experiments and gates

### 7.1 Gates (pass each one before investing in the next stage)

| Gate | Question | Pass criterion | If it fails |
|---|---|---|---|
| **G0 Literature** | Is there a defensible contribution after the comparison with §1.5? | Comparison table done; contribution wording agreed | Reframe as a benchmark/framework study |
| **G-ID Identifiability** (§4.4) | Which quantities can ECG+PPG distinguish? | θ_red recorded with structural and practical evidence | Keep warning prediction; reduce or drop the explanation claims |
| **G1 Pilot (50 cases)** | Is the data suitable? | Audit done of: synchronization, `subjectid` mapping, past-only reference feasibility, eligible time, event yield, censoring, overlap storage, independent CO/SV availability | Revise inclusion, endpoint or lead time **before** the main build. The pilot is not a powered efficacy study |
| **G2 Strong simple comparator** | Is there a real warning problem? | A personalized feature-based temporal predictor (plus a fixed-reference variant) runs in continuous replay with non-trivial event sensitivity at the provisional burden | Revisit the endpoint or lead time |
| **G3 Hybrid** | Does the reduced hybrid add value? | E3 comparison done against an equally personalized data-driven model | Report a negative or neutral result honestly |
| **G-LOCK** | Is the protocol frozen? | Splits, event rules, observation rules, alert policy, thresholds and primary comparisons are frozen and hashed **before** the test set is touched | — |

The 26-week schedule (§8) is a target. The gates decide continuation and scope, not a commitment to finish every experiment.

### 7.2 Experiments

| ID | Question | Setup | Main metrics |
|---|---|---|---|
| **E0** | Identifiability (G-ID) | §4.4 | Rank/sensitivity, posterior geometry, PPC, recovery error (HR reported separately), SBC |
| **E1** | Pilot audit (G1) | 50 VitalDB cases | Eligible-time fraction, events per patient-hour, censoring fraction, timing quality, storage |
| **E2** | Strong simple comparator (G2) | Personalized features + GBM in continuous replay | Event sensitivity at the provisional burden; false alerts per eligible hour |
| **E3 (primary)** | RQ2: hybrid vs equally personalized data-driven | VitalDB test set, continuous replay, frozen policy | **Event-level sensitivity for T-warn at the frozen threshold**; false alert episodes per eligible hour; precision; lead time |
| **E4** | RQ1: adaptation | Fixed anchor vs ordinary EMA vs threshold-frozen EMA vs anchor + EMA (§4.6); CSA-TTA if reproducible; oracle reference reported separately; cold-start subgroup; **gradual-decline** and controlled-sensor-drift subgroups | ΔSensitivity at matched burden; lead time; false alerts |
| **E5** | RQ3: modality | ECG-only / PPG-only / fusion; PAT removed; timing jitter (±8, ±16, ±32 ms); per-modality availability | ΔSensitivity, Δlead time, availability |
| **E6 (primary, explanation)** | RQ4: CES vs comparators (§4.9) | Independent benchmark (§7.3); same classes and information for every method | Risk–coverage curves; **selective error at matched availability**; AURC; forced-label accuracy; unresolved fraction; set size and coverage; competitor recall (when Ê is wrong, is the true mechanism among the non-rejected competitors?); compute per alert |
| **E6b** | RQ5: AAT | Fixed architecture; ordinary (nuisance-complete) training vs AAT; tested on the independent simulator and unseen sensor distortions | Same as E6, plus distinguishable-change detection rate |
| **E6r** | CES on real data (descriptive) | VitalDB test alerts | Explanation availability; PPC pass rate; distribution of competitor types (how often a sensor explanation competes). **No correctness claim** without an independent reference (§3.7) |
| **E7** | U1/U2/U3 calibration | §2 table | Simulated posterior coverage/SBC; Brier score, reliability, slope/intercept; realized alarm burden with CIs |
| **E8** | External validity | MIMIC, synchronization-eligible records (PAT model) and others (timing-agnostic variant) | E3 metrics by source and synchronization status |
| **E9** | Robustness | PPG-DaLiA motion; noise, gain and offset sweeps; missing modality | Observation and prediction availability, timing error, degradation curves (no hypotension accuracy on DaLiA) |

### 7.3 Synthetic scenario design (E6) — avoiding "same-simulator" circularity

- The test scenarios must **not** come only from the simulator used to train the inverse model. They must include:
  - a changed observation model (different filter shape, gain/offset drift);
  - parameter ranges outside the training range;
  - PEP perturbations;
  - combined faults;
  - **unknown faults** (outside the explanation set);
  - **deliberately indistinguishable parameter combinations**, where the correct output is "unresolved".
- **Independent generator:** generate data with a higher-fidelity or independently specified simulator (e.g., a closed-loop or 1D model), even though the deployed model stays simple.
- **Baseline variability:** baseline drift, respiratory and Mayer-wave modulation, and patient variability, with interventions given an onset and a ramp duration.
- **Comparisons under identical information:**
  - physics-only inference;
  - hybrid;
  - a data-driven scenario classifier trained on the same synthetic labels.
- SHAP is only a supplementary explanation analysis of data-driven models. It is **not** a cause classifier and not the H2 comparator.
- **Benchmark release.** Package the scenario set, with ground-truth *compatible sets*, as a reusable benchmark. It contains:
  - indistinguishable mechanisms;
  - sensor changes;
  - combined abnormalities;
  - unknown scenarios;
  - model-mismatch cases.
  - The benchmark is a contribution in its own right, and the fallback if CES gives no advantage.

### 7.4 Comparators (all equally personalized where applicable)

All models get the same history H, the same available inputs, the same supervision and comparable tuning effort.

1. Population thresholds (HR and PPG/PAT features, fixed limits).
2. Personalized feature-based monitoring (z-scores against the past-only reference).
3. **Personalized logistic regression / gradient-boosted model on history features (strong simple comparator)**.
4. Personalized supervised neural forecaster (CNN/GRU over the history).
5. Representation-learning comparator (SNUPHY-M, if reproducible).
6. Physics-only (θ_red + deviation → risk head).
7. Hybrid without residual.
8. **Hybrid (proposed).**
9. ABP-oracle variant (labelled; upper bound only).

### 7.5 Evaluation and statistics

- **Continuous replay** of uninterrupted eligible recordings at their natural prevalence. Never use only sampled event and non-event clips for the primary claims.
- **Report:**
  - false alert episodes per eligible hour and the eligible fraction of total time;
  - event-level and patient-level counts;
  - sensitivity, precision, alert duration and the lead-time distribution.
- **Why α is not an alarm rate:** at a 5 s stride there are 720 evaluations per hour. A per-window exceedance probability of 0.05 means about 36 positive windows per hour, not 36 episodes. The episode count depends on persistence, merging and refractory rules. Alarm burden is therefore defined and controlled **at episode level**.
- **Uncertainty intervals:** patient-clustered (by `subjectid`) paired bootstrap, with at least 1,000 resamples. Window-level DeLong is **not** used for these correlated windows.
- **Pre-registered primary metric** (frozen at G-LOCK): event-level sensitivity for T-warn at the frozen threshold, chosen on calibration subjects for ≤ 1 false alert episode per eligible hour [PROVISIONAL]. Report the realized test burden with its CI.
  - A fixed-budget sensitivity curve on the test set is **descriptive only**, and is kept distinct from frozen-threshold performance.
- **Conformal methods:** ordinary split conformal is not assumed valid for overlapping, drifting series. Sequential-dependence methods (e.g., SPCI) are exploratory, with their assumptions stated. Online schemes that need outcome feedback must respect whether ABP labels would actually be available in the claimed setting (they are not, in the main setting).
- **Subgroups:** age, sex, ASA and surgery type. Analyse failure cases.

### 7.6 Freezing rule

The following are tuned on train, tune and calibration subjects only, and frozen at G-LOCK:
- all [PROVISIONAL] values (`gap_max_s`, `recovery_s`, `merge_s`, `post_event_refractory_s`, `persist_s`, `refractory_s`, H, `ref_minutes`, `ref_halflife_min`, α_e, thresholds);
- event rules;
- the alert policy.

Any later change is recorded in §14 together with the reason, and the test results are rerun and reported as post-hoc.

---

## 8. Implementation phases (adopted plan; there is no deadline, so the gates decide pace)

**Working model**
- Claude writes the code and explains it; the owner reviews.
- Each phase ends with a **review checkpoint**: a short summary of what was built, how to check it, and the results.
- Nothing proceeds past a gate without the owner's OK.

**Where things run**

| Place | Hardware | Used for |
|---|---|---|
| **Local** (Windows, Python 3.13, CPU, no NVIDIA GPU) | CPU | Package code, tests, simulator development, small analyses |
| **Colab-CPU** (free tier) | CPU | VitalDB downloads and preprocessing (data lands on Drive) |
| **Colab-GPU** (free tier, T4) | GPU | Neural training only (NPE, residual, neural comparators, AAT) |

**Python versions:** code must run on both local Python 3.13 and Colab's Python. Pin dependencies that work on both, and check `torch` / `sbi` wheels for each.

**Size tags:** S ≈ 1–2 sessions, M ≈ 3–6 sessions, L ≈ 6+ sessions.

### P0 — Foundations (Local; S)

**Goal:** a working, tested project skeleton that runs identically locally and on Colab.

**Tasks**
- `git init`, `.gitignore` (data, runs, checkpoints, `.ipynb_checkpoints`).
- `pyproject.toml` (package `dtwin`, `src/` layout). Dependency groups are optional extras (`sim`, `signal`, `ml`, `dev`, `all`) instead of a separate Colab requirements file. Exact version pins come once the P1 environment works on both machines.
- `dtwin/utils`:
  - `io.py`: path resolver for local vs Colab/Drive;
  - `seed.py`;
  - `config.py`: YAML loading, merge, and a resolved-config dump;
  - `log.py` (named so it does not shadow the stdlib `logging`);
  - `run.py`: run_id plus saving the git hash and config.
- `configs/base.yaml` holding every [PROVISIONAL] value from this file.
- `notebooks/00_setup_colab.ipynb`: clones or pulls the private GitHub repo (read-only token entered at runtime, never saved in the notebook), then runs `pip install -e .` and mounts Drive.
- `pytest` setup and a `tests/test_smoke.py`.

**Done when**
- `pip install -e .` and `pytest` pass locally.
- The setup notebook runs on Colab and imports `dtwin`.

**Review:** folder structure, config system, how code reaches Colab.

### P1 — Simulator and observation model (Local, CPU; M)

**Goal:** fast, differentiable, batched simulation of ECG timing + PPG (+ ABP) windows with all nuisances.

**Tasks** (in `physics/`)
- `windkessel.py`: WK3 with half-sine inflow, RK4, batched in PyTorch.
- `observation_model.py`: §4.3 — PAT = PEP + PTT_vasc + δ_dev; PPG gain/offset/filter; noise; baseline wander; motion artifacts.
- `ecg_synth.py`: R-peak timing and a simple ECG morphology template. ECGSYN through `neurokit2` is used only for realism checks.
- `simulator.py`: θ + nuisances → (`x_wave`, fiducials, ABP), plus slow-variability trajectories for synthetic patients.

**Tests**
- Positive pressures.
- Steady-state MAP ≈ CO · R_p.
- **The WK3 scaling symmetry gives identical waveforms** (the review's derivation, as a unit test).
- Fiducial and PAT recovery on noise-free signals within 1 ms.
- Speed benchmark (local CPU now; T4 later).

**Done when:** tests pass, and example-waveform plots look physiologically plausible.

**Review:** waveform plots and test results.

### P2 — Identifiability study, gate G-ID (Local; M)

**Goal:** decide θ_red with evidence (§4.4).

**Tasks** (in `identifiability/`)
- Structural: symmetry search plus a sensitivity-matrix rank check (autograd Jacobian across many θ).
- Practical: Fisher information under noise and nuisances; profile likelihoods by constrained optimization; posterior geometry from a quick MCMC on a few cases; prior sensitivity.
- Report: `runs/<id>/identifiability.md`, containing tables, profile plots and the proposed θ_red together with the explanation classes it allows.

**Done when:** the owner approves θ_red and the explanation-class list (`configs/explanations.yaml`). Both are recorded in §14.

**Fail path:** if almost nothing beyond HR and PAT is identifiable, narrow the explanation claim and record it in the decision log.

> P2 does not need any patient data, so it can run while P3 downloads.

### P3 — VitalDB pilot pipeline, gate G1 (Colab-CPU, then local; L)

**Goal:** a clean, causal, audited data pipeline on 50 subjects.

**Tasks**
- `data/vitaldb.py`: case discovery, `subjectid` mapping, track-name verification, chunked download that can resume, continuous storage format (§3.8) on Drive.
- `preprocess/`: causal filters, SQI, fiducials at the native rate (R-peak, PPG foot/peak), observation-availability flags.
- `labels/`: ABP artifact detection, MAP per beat, events (MAP < 65 for ≥ 60 s), recovery, merging, censoring, eligibility.
- `data/report.py`: the pilot audit (G1 list in §7.1), including eligible-time fraction, events per patient-hour, the share of events that leave ≥ 10–15 min of eligible history before onset, storage per case, any CO/SV tracks, and a rejected-data audit.
- **Tests:** a no-look-ahead test for filters and features; event-rule unit tests on hand-made MAP traces.

**Done when:** the pilot report is reviewed, and the cohort size for the full build is chosen from event yield (storage budget below).

### P4 — Splits, replay engine and metrics (Local; M)

**Goal:** an evaluation harness that every model will use, so all comparisons are identical.

**Tasks**
- `data/splits.py`: subject-level train / tune / calibration / test, hashed split files.
- `eval/replay.py`: streams each patient window by window. Models expose `update(window) → risk, state`. Includes a no-look-ahead check.
- `alerts/policy.py` (persistence, merge, refractory) and `alerts/matching.py` (T-warn matching, false-alert episodes).
- `eval/alarm_metrics.py`, `eval/calibration.py` (Brier score, reliability, slope/intercept), `eval/bootstrap.py` (subject-clustered paired bootstrap).
- **Tests:** synthetic risk traces with known correct metric values.

**Done when:** a dummy model runs end-to-end on pilot data and the metric tests pass.

### P5 — Full cohort and strong simple comparator, gate G2 (Colab-CPU + local; M)

**Goal:** prove there is a real warning problem before building the complex parts.

**Tasks**
- Build the full cohort (size from P3).
- `features/` + `features/history.py` (rolling history H).
- `baselines/`: population thresholds, personalized z-scores, **personalized GBM** (LightGBM) risk head, and a fixed-reference variant.
- Train on train, tune on tune, freeze thresholds on calibration.
- Replay on tune/calibration only. **The test set stays untouched.**

**Done when:** G2 is met (non-trivial event sensitivity at the provisional burden).

**Fail path:** revisit the endpoint or lead time now (before G-LOCK).

### P6 — Amortized inference (Colab-GPU; L)

**Goal:** NPE over θ_red with nuisances; well calibrated on simulations, sensible on real data.

**Tasks**
- `inference/embedding.py`, `npe.py` (with `sbi`), and a training script that checkpoints to Drive every N steps and resumes.
- SBC, coverage, contraction (U1); posterior predictive checks on real VitalDB windows (train subjects).
- Sim-to-real check: compare distributions of real vs simulated summary features. Fine-tune only on train subjects.

**Done when:** SBC passes on held-out simulations, and real-data PPC pass rates are reported.

### P7 — Twin state and hybrid risk head, gate G3 (Local + Colab-GPU; M)

**Tasks**
- `twin/reference.py`: past-only anchor + EMA + freeze; cold-start population prior.
- `twin/deviation.py`: z vs EMA and vs anchor, with uncertainty and observation status kept separate.
- `inference/residual.py`: a small conditional AE, plus the absorption test (§4.8).
- `twin/changepoint.py`: BOCPD, with CUSUM as the baseline.
- `risk/risk_head.py`: GBM on hybrid history features, plus recalibration on the calibration subjects.
- Physics-only, hybrid and hybrid-without-residual variants, all run through the P4 harness.

**Done when:** the G3 comparison against the P5 GBM is done (tune/calibration only) and the result is reported honestly.

### P8 — Explanation: CES, comparators, AAT and benchmark (Local + Colab-GPU; L)

**Tasks**
- **Independent generator** (`physics/independent/`): a second, independently specified model, e.g. a closed-loop time-varying-elastance model, a different PPG observation model, and PEP dynamics. It is used **only** to create test scenarios.
- `physics/scenarios.py`: the scenario library (§7.3), with ground-truth *compatible sets*.
- `explain/ces.py` (§4.9): constrained fits warm-started from NPE, gaps, simulation-calibrated rejection, PPC, compute budget.
- `explain/comparators.py`: argmax, posterior mass, posterior SD, profile-likelihood intervals, a selective scenario classifier.
- `inference/ambiguity_training.py`: AAT for the explanation head and classifier; nuisance-complete NPE as the baseline.
- E6, E6b (risk–coverage at matched availability, AURC); E6r on tune/calibration alerts.

**Done when:** E6 and E6b results are reviewed. Then decide between the method framing and the benchmark framing (§1.3).

### P9 — Locked evaluation (Local + Colab; M)

**Tasks**
- **G-LOCK:** write `configs/locked.yaml` with all frozen values and hashes of splits, configs and code commit.
- Run test-set replay **once**: E3–E5, E7, E6r.
- E8 external test on MIMIC waveforms (open access; account not needed for open releases — `TODO(verify)`). Run the synchronization gate first.
- E9 robustness on PPG-DaLiA.
- `scripts/make_tables.py` / `make_figures.py`: every number regenerable.

**Done when:** a results package is ready for the paper (writing itself is deferred, §9).

### Dependency order

```
P0 → P1 → P2 (G-ID) ─────────────┐
 └──→ P3 (G1) → P4 → P5 (G2) ────┴→ P6 → P7 (G3) → P8 → P9 (G-LOCK)
```

P1/P2 (local, simulation only) and P3 (Colab downloads) can run in parallel.

### Storage budget (free Drive, 15 GB)

| Item | Budget |
|---|---|
| ECG + PPG continuous at 125 Hz float16 (+ masks) | ~7 MB per 4-hour case |
| ABP | Per-beat SBP/DBP/MAP for all cases; the full ABP waveform for a ≤ 200-case subset (physics validation) |
| Cohort | ~1,000 cases ≈ 8–9 GB including features and labels. Adjust after the pilot |
| Runs/checkpoints | ≤ 3 GB; prune old runs |

If Drive fills up: lower the cohort size before lowering data quality, and record the change in §14.

### Old milestone map (kept for reference; superseded by P0–P9)

| Phase | Weeks | Deliverable | Gate |
|---|---|---|---|
| M0: Literature + setup | 1–3 | `related_work.md` comparison; repo skeleton; Colab setup; release pinning | G0 |
| M1: Identifiability study | 2–6 | Simulator + observation model; structural and practical analysis; θ_red | **G-ID** |
| M2: Pilot + labels | 3–7 | VitalDB loader, `subjectid` splits, ABP artifact and event rules, censoring, eligibility, fiducials at native rate, 50-case audit | **G1** |
| M3: Strong simple comparator | 6–10 | Personalized feature GBM; continuous replay; alert policy; alarm metrics | **G2** |
| M4: Hybrid | 10–16 | NPE on θ_red; reference state; residual; risk head; distinguishability rule defined | **G3** |
| M5: Explanation study | 14–18 | Explanation classes; CES + comparators; AAT; independent benchmark; E6, E6b | CES beats or matches comparators at matched availability (otherwise use the benchmark framing) |
| M6: Locked evaluation | 18–22 | Freeze (G-LOCK); E3–E5, E7–E9 | **G-LOCK** |
| M7: Writing | 21–26 | Manuscript; reproducibility package | — |

---

## 9. Paper outline (first study) — **deferred by owner; do not start writing**

1. **Introduction:**
   - the alarm-burden problem;
   - personalization vs population thresholds;
   - why the limits of mechanistic interpretability matter;
   - contributions, stated as precisely as G0 allows.
2. **Related work:** §1.5, expanded.
3. **Methods:** observation model and identifiability analysis; reduced hybrid inference; reference state; risk head; alert policy; distinguishability rule.
4. **Experimental protocol:** VitalDB cohort; event, censoring and eligibility definitions; splits; comparators; frozen operating point; statistics.
5. **Results:** E0 → E9.
6. **Discussion:**
   - what the signals can and cannot explain;
   - failure modes;
   - limitations: retrospective replay; perioperative population; PPG observation assumptions; no independent physiological references; no imaging; no ambulatory claim;
   - path to the long-term digital-twin vision.

**Key figures**
1. Observation-model and identifiability diagram, showing the symmetry.
2. Patient timeline: signals, θ_red, reference band, risk, alerts, explanation status.
3. Sensitivity vs false alerts per eligible hour, with the frozen operating point marked.
4. Selective attribution error vs explanation availability (E6).
5. Reliability diagrams (U2).
6. Ablation and modality chart (E4/E5).

---

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Strong overlap with prior work (§1.5) | G0 comparison; empirical or benchmark framing if no method novelty survives |
| Hemodynamic parameters not identifiable (expected from the WK3 symmetry) | G-ID before SBI; reduced θ_red; claims limited to what passes |
| PAT confounded by PEP and device delay | Nuisance modelling; PAT-removal and jitter ablations; no stiffness claims |
| No independent physiological reference | Attribution evaluated in simulation only; audit CO/SV availability |
| Sim-to-real gap | Independent generator; posterior predictive checks on real data; report real and simulated results separately |
| Leakage (subject, provenance, oracle reference, future data) | `subjectid` splits; provenance mapping; past-only rules; causal processing; tests |
| Low event yield, or a weak warning signal at ≥ 10 min | Pilot (G1) and simple comparator (G2) before the full build; protocol revision only before testing |
| External sites lack synchronization | Synchronization gate; timing-agnostic variant; limited transportability claim |
| Colab limits | Resumable chunks; small models |

---

## 11. Working conventions (for Claude and humans)

- Logic lives in `src/dtwin/`; notebooks only orchestrate and plot.
- Configs, not constants. Every [PROVISIONAL] value lives in `configs/`.
- Paths go through `dtwin.utils.io` only. Never hardcode `E:\`, `C:\` or `/content` in package code.
- **Subject-level splits only.** Code that touches data takes the saved split files as input.
- **No look-ahead.** Every streaming component (filters, features, reference, risk head, alert policy) has a test showing its output at time t is unchanged when future data are altered.
- **No oracle leakage.** ABP and event labels never feed inference-time components in the main setting.
- Separate status fields: observation availability, prediction availability, explanation availability.
- Never interpret non-identifiable parameters physiologically. Never present priors as observed information.
- Units: mmHg, mL/s, s, mmHg·s/mL, mL/mmHg. Document them in docstrings.
- Every table and figure is regenerable from a script plus a config. No hand-edited numbers.
- **Never fabricate results, citations or dataset details.** Unverified items are marked `TODO(verify)`.
- Data governance: never commit, upload or print raw patient-level data from credentialed sources. Respect each dataset's licence.
- **Notebooks are committed without outputs.** Running a notebook in VS Code saves its outputs into the file, so check `git diff` and strip outputs before committing. Never use `git commit -a` blindly on notebooks.
- **Git:** Claude may commit and push to the project's GitHub repo. **Never** add Co-Authored-By or any other attribution line to commits or PRs.
- **Working style:** Claude builds and explains in simple words; the owner reviews. Stop at every phase checkpoint and gate (§8) for review.

---

## 12. Open decisions (owner input needed)

- [x] Adopt v2 and v2.1 — **adopted 2026-10-24**.
- [x] **Owner answers (2026-10-24):**
  - Journal paper, no deadline.
  - Solo: no supervisor, **no clinician**.
  - Endpoint settings delegated to Claude.
  - Claude builds and explains; the owner reviews.
  - Colab free tier.
  - GitHub OK; commit without attribution; never push.
  - No PhysioNet account.
  - Do not start the paper yet.
- [x] **Endpoint decision (by Claude, as delegated):**
  - Keep MAP < 65 mmHg for ≥ 60 s.
  - T-warn = onset in [t + 10, t + 15] min.
  - ≤ 1 false alert episode per eligible hour.
  - All three remain [PROVISIONAL] until G-LOCK, and are revisited after the P3 pilot.
- [x] **Consequence of having no clinician:**
  - Event, artifact and eligibility rules follow published definitions, and each rule's source is cited in `configs/events.yaml`.
  - The paper states the absence of clinical adjudication as a limitation.
  - Explanation correctness is claimed in **simulation only**. No L3 (clinical cause) output.
- [ ] Physics depth: WK3 or simpler, decided at G-ID (P2).
- [x] Code transfer to Colab: the owner's **public** GitHub repo, https://github.com/plufle/Patient-adaptive-ECG-PPG-hypotension-warning-with-competing-explanation-search. Claude commits and pushes (no attribution). Colab clones it without a token.
  - **Commit cadence (Claude's choice):** small commits within a phase; push at each phase checkpoint once tests pass.
  - The plan is public, so never commit data or anything derived from credentialed datasets.
- [ ] Deliverable type (thesis, journal or conference), deadline and readership. The review suggests one biomedical-engineering methods study, with the venue chosen after the pilot.
- [ ] PhysioNet: pin the exact waveform releases. Linked-EHR credentials are needed only if EHR variables are used. Current status is unknown.
- [ ] Clinical collaborator to review event, censoring and eligibility rules, the reference-state rule and the permissible explanation vocabulary.
- [ ] Confirm the primary endpoint (hypotension, T-warn at 10–15 min) and the provisional burden (1 false alert per eligible hour).
- [ ] Physics depth: WK3 or simpler, pending G-ID.

## 13. Status

- 2026-10-24: v1 drafted.
- 2026-10-24: external scientific review received ([RESEARCH_PLAN_REVIEW_2026-10-24.md](RESEARCH_PLAN_REVIEW_2026-10-24.md)). Plan revised to v2; v1 archived. No code or data yet.
- 2026-10-24: v2.1. Second review note added the contribution direction: Competing-Explanation Search (main), Ambiguity-Aware Training (training component), anchored adaptation and measurement selection (alternatives). New prior work added to §1.5 (unverified).
- 2026-10-24: owner adopted v2.1. The owner asked **not to start implementation yet**. Open questions are being collected (§12).
- 2026-10-24: owner answered the §12 questions. Implementation phases P0–P9 planned (§8). Implementation **not started**.
- 2026-10-24: **P0 built**: package skeleton, utils (paths, config, seed, log, run), `configs/base.yaml`, Colab setup notebook, README, tests. 14 tests pass locally (Python 3.13). Committed locally. The first push needs the owner to log in to GitHub once in their own terminal.
  - Still open: the Colab notebook has not yet been run on a Colab runtime (owner to run it).
- **Next:** owner reviews P0 and runs `00_setup_colab.ipynb` on Colab. Then P1 (simulator). Then M0 (related-work comparison, repo skeleton, Colab setup) and M1 (simulator + identifiability study) start in parallel.

## 14. Decision log

| Date | Decision | Status | Reason |
|---|---|---|---|
| 2026-10-24 | Core modalities ECG + PPG; ABP for targets and adjudication only; imaging deferred | Adopted (v1) | Feasibility with public data |
| 2026-10-24 | VitalDB as primary dataset | Adopted (v1) | Open; long multimodal recordings; frequent hypotension |
| 2026-10-24 | Colab GPU via VS Code extension; installable package; data on Drive | Adopted (v1) | No local GPU |
| 2026-10-24 | Narrow the first study to hypotension warning plus explanation reliability; digital twin as long-term vision | Adopted (v2) | Prior-work overlap; intraoperative data cannot establish normal physiology |
| 2026-10-24 | Split by `subjectid`; PulseDB provenance exclusion; four-way split with a calibration set | Adopted (v2) | Leakage control |
| 2026-10-24 | Identifiability gate before SBI; reduced θ_red; no physiological interpretation of non-identifiable parameters | Adopted (v2) | WK3 SV/R/C/Z_c scaling symmetry (derivation in §4.4, checked) |
| 2026-10-24 | PAT (not PTT); PEP and device delay as nuisances; fiducials at native rate | Adopted (v2) | PAT includes PEP; 8 ms resolution at 125 Hz |
| 2026-10-24 | Three-level explanations with "unresolved"; no clinical cause labels without independent reference | Adopted (v2) | Model has no contractility/volume states; ABP is not independent truth for SV/R |
| 2026-10-24 | Add a risk head; T-warn = onset in [t+10, t+15] min; episode-level alarm metrics; frozen thresholds | Adopted (v2) | The present-state detector is not a forecaster; α ≠ alarm rate |
| 2026-10-24 | Equally personalized comparators, including GBM; data-driven scenario classifier instead of SHAP for attribution | Adopted (v2) | Fair test of whether the physics adds value |
| 2026-10-24 | Store continuous signals and slice windows on the fly | Adopted (v2.1) | Avoids ~2× overlap storage |
| 2026-10-24 | Main contribution = Competing-Explanation Search; explanation becomes the primary question and warning a co-primary non-inferiority requirement | Adopted (v2.1) | A concrete, falsifiable method; more specific than a confidence threshold |
| 2026-10-24 | Ambiguity-Aware Training as the training component; baseline must be nuisance-complete NPE | Adopted (v2.1); baseline caveat by Claude | A correctly specified NPE already learns non-identifiability, so the fair test is against it |
| 2026-10-24 | Always also report the fixed-anchor deviation; anchored adaptation (A3) and measurement selection (A4) kept as alternatives | Adopted (v2.1) | EMA can absorb slow deterioration |
