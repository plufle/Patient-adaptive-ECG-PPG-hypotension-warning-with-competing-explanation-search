# Research-plan validation and proposed decisions

Review date: 24 October 2026. Inputs: the complete `CLAUDE.md` and the attached aim/novelty image. This is a scientific review, not experimental validation. No code, data, or results currently exist in the workspace. `CLAUDE.md` has not been changed; all decisions below are recommendations pending adoption.

## Assessment

Continue the project, but revise the scientific specification before implementation. The engineering outline is useful. The broad four-pillar novelty claim, physiological source-identification promises, and calibration claims are not yet defensible. A feasible first study is retrospective ECG–PPG monitoring for perioperative hypotension, with patient adaptation and explicit limits on physiological explanation.

The attachment states a long-term vision involving imaging, wearables, multiple abnormalities, and physiological causes. The actual first study should make a narrower claim. Intraoperative recordings cannot establish a person's normal physiology in everyday life. Use “individual reference state” or “patient-specific perioperative baseline” rather than “normal physiology.”

The literature search found substantial overlap, including uncertainty-based rejection and sequential physiological updating. Therefore neither the four-component combination nor adding abstention is enough, by itself, to establish novelty. The proposed gap below is a research direction to test, not a verified first-in-field claim. This was a targeted literature review, not a systematic search.

## Closest prior work and its implications

| Primary source | Relevant overlap | Implication for this project |
|---|---|---|
| [Wehenkel et al., Simulation-based Inference for Cardiovascular Models (2023; revised 2024)](https://arxiv.org/abs/2307.13918) | Cardiovascular neural posterior inference, uncertainty and ambiguous parameter solutions | SBI, posterior uncertainty, and observing non-identifiability are established ingredients. |
| [Manduchi et al., Leveraging Cardiovascular Simulations for In-Vivo Prediction of Cardiac Biomarkers (2024 preprint)](https://arxiv.org/abs/2412.17542) | Hemodynamic SBI, simulated PPG analysis, real VitalDB evaluation, hybrid learning, and uncertainty-based measurement rejection | This overlaps strongly with the inference plan. Its real-data monitoring analyses include arterial-pressure inputs; do not describe all of its results as ECG–PPG-only. Rejection of uncertain measurements is also prior work. |
| [Zhang et al., PMB-NN (2026 journal article; 2025 preprint)](https://www.sciencedirect.com/science/article/pii/S0169260726002336) | Personalized PPG monitoring with Windkessel constraints and neural networks; acknowledges limits on independently identifying resistance and compliance | Personalized hybrid PPG physiology is not a new contribution by itself. Compare the proposed online updating and warning behavior directly. [Author preprint](https://arxiv.org/abs/2512.10745). |
| [Park et al., SNUPHY-M (2025 preprint)](https://arxiv.org/abs/2509.08830) | ECG/PPG/ABP pretraining and noninvasive hypotension prediction, including VitalDB horizons of 5, 10 and 15 minutes | Multimodality and these horizons are established. Include a reproducible representation-learning comparator where feasible. [Authors' reported code location](https://github.com/Vitallab-AI/SNUPHY-M). |
| [Tong et al., InVAErt networks for amortized inference and identifiability analysis of lumped-parameter haemodynamic models (2025)](https://arxiv.org/abs/2408.08264) | Amortized inverse modeling and non-identifiability in lumped cardiovascular models | “Identifiability-aware” is not sufficient as an unqualified novelty claim either. The contribution must specify a new decision rule, evaluation, or demonstrated benefit. |
| [Thiel et al., WCCM–ECCOMAS 2026 conference abstract](https://wccm-eccomas2026.org/event/contribution/8bb62944-efb5-11f0-b205-000c29ddfc0c) | Bayesian 0D hypotension modeling, sequential parameter updating, and scenario-dependent treatment analysis | Sequential updating and uncertainty around hypotension mechanisms are also being studied. This is an abstract, and it states that real-patient validation is a next step; it is not evidence of established clinical efficacy. |

These papers have different scopes and evidence levels. Their overlap weakens the current general novelty wording; it does not establish that the proposed complete study has already been done.

## Recommended research question and scope

**Primary question:** In held-out adult surgical patients, does a patient-adaptive ECG–PPG model informed by identifiable hemodynamic structure improve event-level hypotension warning sensitivity at a prespecified false-alarm burden compared with equally personalized data-driven models?

“Equally personalized” is essential: beating a fixed population threshold would not show that the mechanistic model adds value.

| Question | Testable hypothesis | Required evidence |
|---|---|---|
| RQ1: Does adaptation help? | Past-only patient adaptation improves event sensitivity at the chosen alarm budget relative to the same model with adaptation disabled. | Paired continuous replay, identical eligibility and alert policies, patient-clustered confidence intervals. |
| RQ2: Does physiology add useful information? | A reduced hybrid model improves warning sensitivity or probability calibration relative to a personalized data-driven model with the same inputs, history, and supervision. | Physics-only, data-only, hybrid, and hybrid-without-residual comparisons. Parameter count is secondary. |
| RQ3: When does ECG add value to PPG? | Fusion improves warning performance in prespecified conditions, and the gain changes when timing information is removed or corrupted. | Matched modality ablations, a PAT-removal ablation, timing-jitter tests, and monitoring-availability reporting. Do not assume PAT is the dominant contributor. |
| RQ4: When is a physiological explanation justified? | A rule that reports an explanation only when competing model explanations can be separated reduces incorrect confident attributions under noise, ambiguous causes, and model mismatch. | Independent synthetic scenarios with known interventions; selective attribution error versus explanation availability; real-data validation only where independent references exist. |

Treat event-risk calibration, parameter-posterior calibration, and alarm burden as distinct evaluation requirements. A single “90% coverage” hypothesis cannot validate all three.

**Proposed aim:** To develop and retrospectively validate a patient-adaptive ECG–PPG model for early warning of intraoperative hypotension, and to quantify when the available signals support a physiological explanation of the detected change.

**Candidate novelty wording:** This study will test whether limiting online physiological explanations to changes distinguishable from the available ECG–PPG signals improves explanation reliability while preserving useful hypotension warnings under patient variability, sensor corruption, and model mismatch.

That wording proposes an empirical contribution. To make a method contribution, define the explanation rule mathematically and compare it with ordinary posterior-uncertainty thresholding and existing hybrid inference. If the final method is only a collection of existing components, describe the contribution as a validated monitoring framework and benchmark rather than inventing an algorithmic novelty claim.

## Scientific changes required before implementation

### 1. Resolve the structural ambiguity in the current simulator

Affected: `CLAUDE.md` §§4.3–4.4, 4.7, E0 and E1.

For the specified WK3 equations, keep HR, ejection time and waveform shape fixed. For any positive scale factor a, transform

    SV' = a SV
    R_p' = R_p / a
    C' = a C
    Z_c' = Z_c / a
    Q'(t) = a Q(t)

Then

    C' dP_p/dt = a [Q - P_p/R_p]
    P_ao' = P_p + (Z_c/a)(aQ) = P_ao.

With the same initial pressure, the pressure waveform is unchanged. The proposed delayed/filtered PPG is consequently unchanged too. This is a direct derivation from this plan's equations, not a result from a downloaded dataset. It applies when these quantities are jointly free and no independent flow/volume measurement constrains them.

Consequences:

- ECG+PPG cannot uniquely determine every named parameter in this configuration. Even observing pressure does not resolve this particular symmetry when inflow scale is unknown.
- Fixing arbitrary parameters removes degrees of freedom mathematically; it does not establish that the fixed values are correct for an individual patient.
- Clinical priors can regularize the answer. They must not be presented as new information observed in the waveform.
- Candidate parameter combinations such as R_p C may be more defensible than separate absolute parameters, but their identifiability still needs testing under the complete PPG observation model and nuisance variables.

Perform structural analysis first, then practical analysis with noise, sensitivity/rank checks, posterior geometry, prior sensitivity, posterior predictive checks and held-out recovery error. Retain SBC, but do not treat SBC or recovered-versus-true correlation as proof of identifiability or clinical validity. HR is directly measurable and should not dominate an apparent parameter-recovery success.

The [cardiovascular mechanistic-modeling guidelines](https://pmc.ncbi.nlm.nih.gov/articles/PMC11442102/) explicitly recommend establishing parameter identifiability and avoiding biological interpretation of nonunique estimates.

### 2. Replace PTT claims with measured PAT and model the missing delays

Affected: §§1.1, 2, 4.2–4.3 and the mechanism table.

ECG R-peak to PPG foot is pulse arrival time (PAT). It includes a pre-ejection component as well as vascular transit. It is not an independently measured pulse transit time (PTT). An [experimental study of PAT and BP](https://pmc.ncbi.nlm.nih.gov/articles/PMC8611024/) illustrates why pre-ejection changes matter.

Include pre-ejection delay, acquisition latency and timing uncertainty in the observation model, or explicitly restrict interpretation to measured PAT. Do not translate a short PAT directly into arterial stiffening. Correct device delays without removing the physiological delay that the model is intended to study. At 125 Hz, one sample is 8 ms; preserve higher-rate timing where available or validate sub-sample estimation and report timing error.

### 3. Remove unsupported clinical cause labels

Affected: RQ2/H2a, §4.7 and the fault library.

Low inferred SV with rising HR does not uniquely establish hypovolemia. Low inferred SV with stable HR does not uniquely establish reduced contractility. The current WK3 model does not explicitly represent ventricular contractility or circulating blood volume. A rule assigning those labels is a modeling hypothesis, not a recovered clinical cause.

Use three levels of output: observed change; model-compatible explanation or explanation set; clinical cause only when independently validated. Preserve an “unresolved” explanation. A hypotension warning may still be issued when its mechanism is unresolved; explanation abstention must not automatically suppress the warning.

ABP provides pressure-event labels and waveform references. ABP alone does not supply independent ground truth for SV, resistance, preload or contractility. If another monitor provides CO/SV in a subset, identify its measurement method and limitations. A quantity computed from the same pressure model is a model-derived reference, not independent physiological truth. Drug administration or fluid delivery is contextual evidence, not a definitive cause label.

### 4. Add an actual forecasting component

Affected: §§3.4a, 4.4–4.6 and E2.

A current-window posterior, deviation score and change-point detector do not specify a future-event predictor. Add a clearly defined temporal risk head or a validated state-transition/forecasting model. State the observed history length and the future target. A finite-history risk head is a feasible first implementation; full mechanistic forecasting is optional.

Define the difference between present-event detection, prediction within a future horizon, and a warning with a minimum lead time. “Event within 10 minutes” can count an alarm seconds before onset; it does not mean “10 minutes early.” For a primary claim requiring at least 10 minutes of warning, one concrete proposed matching interval is 10–15 minutes before onset. If the pilot supports only a shorter interval, revise the protocol before final testing rather than relabeling the result.

If a Bayesian filter is used, account for shared observations in overlapping windows instead of treating every overlapping likelihood as independent. A per-window posterior plus an EMA is not automatically a sequential physiological state posterior.

### 5. Separate the three uncertainty claims

Affected: H4, §§4.4, 4.6–4.7 and E6.

- **Parameter uncertainty:** assess simulated posterior coverage, contraction and SBC, plus sensitivity to priors and model mismatch. Simulated calibration does not establish real physiological coverage.
- **Event-risk uncertainty/calibration:** use held-out Brier score, reliability curves, calibration slope/intercept and discrimination. ECE may supplement these with its binning specified.
- **Alarm performance:** measure false alert episodes per eligible monitoring hour, event sensitivity, precision, alert duration and lead time in continuous replay.

Ordinary split-conformal validity relies on assumptions that overlapping, drifting time series do not automatically satisfy. [SPCI](https://proceedings.mlr.press/v202/xu23r.html) is an example of a method designed for sequential dependence, with its own assumptions and coverage target. It does not automatically solve clinical event-alarm control. Online schemes requiring outcome feedback must also respect whether ABP labels would actually be available in the claimed inference setting.

At a 5-second stride there are 720 evaluations per hour. A valid marginal normal-window exceedance probability of 0.05 corresponds to an expected 36 positive windows per hour. These are not 36 distinct alert episodes. Persistence, merging and refractory policies change the episode count. Thus alpha = 0.05 is not an hourly alarm-rate specification.

Retain 1 false alarm/hour only as a provisional research operating point, not a clinical acceptability claim. Select thresholds on development/calibration patients, freeze them, and report the realized burden and uncertainty on test patients. A fixed-budget sensitivity curve on test can be descriptive, but is distinct from performance of a deployable frozen threshold.

In §4.6, increasing posterior variance can shrink the deviation score. Report uncertainty and observation failure separately so that uncertain deterioration is not silently classified as normal. Report prediction availability and explanation availability separately.

### 6. Prevent leakage across calibration, pretraining and external testing

Affected: §§3.1, 3.4 and 4.5.

- Group VitalDB splits by **subjectid**, not caseid. Its [dataset paper](https://www.nature.com/articles/s41597-022-01411-5) distinguishes 6,388 operations from 6,090 people. All operations from one person belong to the same split.
- Resolve original patient provenance across raw data and derived PulseDB data before any pretraining. PulseDB–VitalDB can overlap held-out VitalDB; PulseDB–MIMIC can contaminate a proposed MIMIC external test. “Unsupervised” pretraining does not remove this concern.
- Separate model tuning, calibration/threshold selection and final testing. The existing validation share can be subdivided or cross-fitted; a particular new split ratio is not mandated here.
- At inference, build the patient reference from a fixed, past-only ECG–PPG rule. Selecting the “first stable 15–30 minutes” using test ABP or future event labels creates an oracle calibration setting. If reported, label it separately.
- Use a population fallback and report cold-start performance when no usable personal reference exists. Do not discard these patients silently.
- Restrict static variables to what is available at the prediction time. Whole-operation drug totals, subsequent outcomes or postoperative tests are not baseline predictors.
- Ensure filters, resampling, imputation and feature extraction use only data available at the stated alert time. Report any buffering delay.

### 7. Fix the external-validation and wearable claims

The [PulseDB paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC9944565/) reports inconsistent inter-signal misalignment of up to 500 ms in its MIMIC-III source and recommends VitalDB-derived segments for analyses requiring precise alignment. Verify timing per external source. Do not assume that a successful cross-correlation alignment recovers true PAT, since it can also remove physiological delay.

Use external data with independently verified synchronization for the full PAT-dependent model. If that is unavailable, explicitly validate a timing-agnostic variant and limit the transportability claim. Report performance by source and synchronization eligibility.

The [current PulseDB repository](https://github.com/pulselabteam/PulseDB) is v2_0 and adds timestamps and non-normalized signal fields. Therefore §3.1a's blanket statement that segments cannot support patient baselines is too strong. Temporal reconstruction may be possible where provenance, continuity and gaps are available, but the selected clips and removed intervals still do not automatically constitute an unbiased continuous alarm benchmark. Raw VitalDB remains the preferred primary replay source.

[PPG-DaLiA](https://archive.ics.uci.edu/dataset/495/ppg-dalia) supports activity/motion and heart-rate evaluation. It does not supply the continuous BP-event or independently adjudicated mechanism targets required here. Use it for signal-quality, timing and observation-availability robustness; do not report clinical hypotension accuracy from it. Its short sessions also cannot provide the proposed first-day baseline. Ambulatory clinical validation requires a separate suitable dataset or study.

The [MIMIC-III matched waveform release](https://physionet.org/content/mimic3wdb-matched/1.0/p01/) and [MIMIC-IV waveform release v0.1.0](https://physionet.org/content/mimic4wdb/0.1.0/) describe open waveform access under their listed licenses. Linked EHR access is a separate question. Pin the exact release and verify its requirements; do not treat all MIMIC data as either uniformly open or uniformly credentialed. The owner's credential status remains unknown.

### 8. Make experiments capable of disproving the claims

Affected: §§7.1–7.5.

SHAP explains feature contributions to a model prediction; it is not a physiological cause classifier. Remove “source attribution versus SHAP” as the primary H2a comparison. Train a data-driven scenario classifier on the same synthetic labels, and compare it with physics-only and hybrid inference under identical information. SHAP can remain a supplementary explanation analysis.

Avoid evaluating only faults created by the same simulator used to train the inverse model. Include changed observation models, held-out parameter ranges, pre-ejection perturbations, gain/offset changes, combined faults, unknown faults, and deliberately indistinguishable parameter combinations. A higher-fidelity or independently specified simulator is a useful test generator even if the deployed model stays simple. Report forced-label accuracy alongside selective error, unresolved fraction and explanation-set size/coverage.

For personalization compare population thresholds, personalized feature-based monitoring, personalized supervised data-driven forecasting, and the personalized hybrid. Give all comparable models the same history, available inputs, supervision and tuning effort. Include a simple logistic/boosted-feature model, not just neural baselines. If continuous ABP is added as an oracle benchmark, label its extra input clearly and do not use it to establish ECG–PPG superiority.

For the real endpoint use MAP <65 mmHg sustained at least 60 seconds as the proposed research label, subject to clinician review. Specify artifact handling, continuity/gap rules, event-end/recovery criteria, event merging, warning matching, persistence and refractory intervals before final evaluation. End-of-record periods without sufficient future observation must not be labeled as certain negatives. Account for recurrent events and report treatment context without interpreting observational associations as treatment effects.

Evaluate uninterrupted eligible recordings at their natural prevalence, rather than only sampled event/non-event clips. Define false alerts as episodes with no matched event in the specified future interval. Report false alarms per eligible hour together with the fraction of all recorded time that was eligible. Report patient- and event-level counts. Use patient-clustered paired bootstrap for comparisons; ordinary window-level DeLong inference is not adequate for heavily correlated windows. Use the pilot to estimate precision and event yield rather than selecting the final cohort size from storage alone.

### 9. Correct smaller feature and feasibility issues

- Single-channel PPG amplitude is not SpO2. Remove “SpO2-like PPG amplitude” from §7.3. Amplitude and DC level are device- and contact-dependent nuisance variables as well as possible physiological information.
- Keep “perfusion-index proxy” conditional on access to an appropriate raw AC/DC measurement; a high-pass-filtered normalized pleth waveform alone does not recover a device's calibrated perfusion index.
- Treat 10-second HRV estimates as ultra-short measurements. Longer rolling histories are preferable for the primary temporal feature set, with short-window variants validated separately. [Research on 10-second RMSSD](https://pmc.ncbi.nlm.nih.gov/articles/PMC10213655/) supports conditional use, not rejection of every ultra-short feature.
- QT/ST and dicrotic-notch features require their own reliability checks under the chosen filtering and sampling. Do not promise diagnostic ECG interpretation from the planned morphology proxies. A 50/60 Hz notch after a 40 Hz low-pass should be justified rather than included automatically.
- Do not use a hard “plausible MAP 40–150” band or ECG–PPG disagreement as an unconditional artifact rule; genuine severe pressure events and pulse deficits can violate these checks. Audit rejected data and disease-dependent exclusions.
- Make the residual model small and validate that it does not absorb the physiological changes the mechanistic component is intended to explain. When the posterior is multimodal, check posterior predictive simulations rather than relying only on a potentially implausible posterior-mean parameter vector.
- The approximate 10 MB storage estimate for three nonoverlapping 4-hour float16 signals is reasonable (10.8 MB in decimal units). Saving overlapping windows at a 5-second stride roughly doubles waveform storage before compression and adds masks, labels and metadata. Revise the processed-data budget accordingly.

## Recommended decisions on the owner's open items

| Decision | Recommendation now | What remains unresolved |
|---|---|---|
| Paper/thesis and venue | Scope the initial deliverable as one biomedical-engineering methods study. Choose venue after the pilot shows the type and strength of evidence. | Owner must specify thesis requirements, deadline and intended readership. No venue or acceptance likelihood is validated here. |
| PhysioNet credentials | Verify the exact waveform release immediately; apply for linked EHR access only if those variables are actually needed. | Actual credential status is unknown. |
| Physics depth | Retain a reduced WK3 or simpler observation model for the first inference study; make parameter reduction an early decision gate. | Which quantities survive identifiability analysis. Escalate to a closed-loop model only for a specific validated need and available measurements. |
| Clinical collaborator | Arrange clinical review of labels, reference-state rules and permissible explanations before clinical cause claims. | Identity and availability cannot be inferred. Without independent clinical references, retain simulated scenario attribution only. |
| Wearable dataset | Keep DaLiA as a secondary motion/signal-quality stress test. | A real ambulatory warning claim needs a separate endpoint-appropriate dataset. Do not add that claim to the first paper. |
| Primary endpoint | Hypotension only; defer AF, hypertension, ischemia and general cardiac-abnormality detection. | Arrhythmia datasets may support a separate later study. They do not validate multimodal physiology in this first cohort. |
| Calibration/input setting | Main study: ECG+PPG only at inference, ABP for training targets and retrospective outcome adjudication. | If initial cuff BP is added, report a separately named calibrated setting. Cuff BP alone does not resolve the SV/R/C scaling symmetry. |
| Digital-twin terminology | Use “retrospective hemodynamic digital-twin prototype” only after demonstrating patient-specific state updating and predictive checks; otherwise use “patient-adaptive hybrid monitoring model.” | Neither anatomical fidelity nor prospective deployment has been established. |

## Revised first-stage work and continuation gates

1. **Literature and mathematical gate, before SBI:** complete a contribution-by-contribution comparison with the closest work; establish which quantities the chosen observation model can and cannot distinguish. If the model cannot distinguish mechanisms, retain warning prediction and revise the explanation claim.
2. **50-case feasibility pilot:** audit synchronized signals, subject identifiers, past-only calibration, usable recording time, event counts and overlapping-window storage. Do not treat this pilot as a powered efficacy study.
3. **Strong simple comparator:** run a personalized feature-based temporal predictor and fixed-reference variant in continuous replay. Establish a real warning problem before building the full inference stack.
4. **Reduced hybrid:** add the mechanistic component, measured PAT and nuisance model only after the first gates. Compare against equally personalized data-driven forecasting.
5. **Explanation evaluation:** quantify ambiguity and explanation availability on independent synthetic scenarios. Add real physiological attribution only for an independently supported subset.
6. **Locked evaluation:** freeze splits, event definitions, observation rules, thresholds and primary comparisons; then run internal and appropriately qualified external tests.

The existing 26-week schedule is a provisional implementation target. E0, event yield, synchronization, clinical reference availability and external-data eligibility should determine continuation and scope, not a commitment to finish all E1–E7 regardless of evidence.

## Proposed change map for CLAUDE.md

| Sections | Proposed revision |
|---|---|
| §1 and attached aim/novelty | Keep broad cardiovascular monitoring as the long-term vision; replace the first-study aim and candidate novelty with the narrower wording above. |
| §2 | Replace H2a's SHAP cause comparison, qualify mechanistic interpretation, separate prediction and calibration questions, and remove presupposed PAT dominance. |
| §3 | Split by subjectid; add provenance checks, independent calibration data, a precise lead-time target, censoring rules and an external synchronization gate. |
| §4 | Reduce the parameter space; account for PEP and device delay; add forecasting; define past-only baseline adaptation and separate unresolved mechanism from no warning. |
| §7 | Add personalized strong baselines, independent-generator/ambiguous-scenario tests, event-level alarm definitions, and separate posterior/risk/alarm calibration. |
| §§8 and 10 | Put identifiability, event yield and data suitability gates before large implementation work. |
| §§12–14 | Record owner choices only when adopted; do not silently convert these recommendations into approved project decisions. |

This review preserves the original plan and its numerical specifications as the record under review. Suggested numerical examples, narrowed hypotheses and new protocol definitions are explicitly proposed changes, not measured results or approved replacements.
