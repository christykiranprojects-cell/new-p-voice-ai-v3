# Deterministic Speech-to-Text Pipeline for Pharmaceutical Voice Orders

## Project Overview

This repository contains the complete implementation of a **deterministic, phase-based Speech-to-Text (STT) pipeline** designed for **pharmaceutical voice order processing** under **regulated (GxP-aligned) environments**.

The system is intentionally engineered to **avoid opaque (black-box) automation**. Instead, it prioritizes:
- Deterministic execution
- Auditability and traceability
- Explainable transformations
- Human-in-the-loop correction
- Compliance with **ALCOA+ data integrity principles**

The pipeline processes real-world voice orders captured via mobile devices and converts them into **business-correct, structured medicine orders** with measurable accuracy and explicit failure auditing.

---

## Key Design Philosophy

This project follows a **system-engineering-first approach**, not just pure end-to-end AI approach.

Core principles:
- **Control Plane ≠ Data Plane**
- Heavy AI workloads are **explicitly governed**, not implicitly executed
- Errors are **measured and logged**, not hidden
- Quantity correctness is treated as a **protected invariant**

In regulated pharmaceutical workflows, **traceability and safety are prioritized over raw automation accuracy**.

---

## High-Level Architecture

The pipeline is organized into clearly defined phases:

```
_________________________________________________________________________________________________________________
 _______________
|               |                              Execution Controller Agent
| CONTROL PLANE |                                (Loading Heavy Model)
|_______________|                           Allocation of Threads/Processors
_______________                                         |
|              | Pre-Phase A   →      Phase A        →    Phase B      →      Phase C     → Phase D   →  Phase E
|  DATA PLANE  |   (Assess)       (Processed Audio)   (ASR-Transcribe)   (Boundary Rules)   (Fuzzy)      (Audit)
|______________|
_________________________________________________________________________________________________________________
                [MEASUREMENT]                           [TRANSFORMATION]
_________________________________________________________________________________________________________________
```

Each phase produces immutable artifacts and never mutates upstream outputs.

---

## Control Plane — Execution Controller Agent

The **Execution Controller Agent** governs all heavy computation.

Responsibilities:
- Enforces a Finite State Machine (FSM): `IDLE → THINK → ACT OR EMERGENCY`
- Controls CPU thread usage
- Owns the Whisper model lifecycle
- Prevents autonomous or unsafe execution

> **Important:** Phase B (transcription) can never load or run Whisper independently. All transcription is injected and authorized by the agent.

This design supports:
- CPU safety
- Deterministic execution paths
- Computer System Validation (CSV)

---
[MEASUREMENT]
## Pre-Phase A — Audio Quality Assessment (Quality Matrix) - 

A **read-only assessment layer** that evaluates audio *before* any preprocessing.

Metrics include:
- Integrated LUFS
- Momentary LUFS
- Silence ratio
- Residual DC offset
- Duration and channel count
- Demoising

Outputs:
- `quality_metrics_report.csv`
- LUFS corridor visualization

This layer ensures evaluation validity by separating **measurement** from **transformation**.

---
[TRANSFORMATION]
## Phase A — Audio Preprocessing 

Deterministic signal processing to produce a canonical audio format:
- 16 kHz sampling OR 16000 HZ
- Mono channel
- 16-bit PCM WAV Format expected for AI Works

Operations include:
- DC offset removal: No Non-Zero
- Loudness normalization: -14 to -24
- Silence trimming
- Conservative denoise placeholder

Phase A is:
- Stateless
- Configuration-driven
- Non-ML

---

## Phase B — Transcription (Whisper)

Speech recognition is performed using **Whisper Large-v1**, executed under strict control.

Key constraints:
- Model loading only in `ACT` state [FSM]
- CPU threads governed by agent [FSM]
- Transcription outputs are immutable [artifacts]

This phase converts normalized audio into **raw transcription artifacts**.

---

## Phase C — Structured Boundary Extraction

A **rule-based NLP layer** that converts raw text into structured medicine items.

Features:
- Deterministic BEGIN–MID–END boundary logic
- Frozen medicine-type alias registry
- Explicit quantity extraction
  
```
RAW_MEDICINE_DOSAGE | RAW_MEDICINE_TYPE | QUANTITY
```

No machine learning or embeddings are used in this phase.

---

## Phase D — Fuzzy Canonical Mapping

An **explainable fuzzy similarity layer** that maps extracted medicines to a master catalog.

Characteristics:
- Token-based similarity (RapidFuzz)
- Variant-preserving normalization
- Deterministic scoring
- Quantity is never modified

This phase resolves spelling and pronunciation variability without introducing hallucinations.

---

## Phase E — Evaluation & Audit

A read-only evaluation layer that measures system performance.

Metrics include:
- True Positives (TP)
- False Negatives (FN / Type II errors)
- Accuracy, Recall, Precision, F1-score
- Quantity MAE
- Word Error Rate (WER)
- Character Error Rate (CER)

All failures are:
- Logged
- Categorized
- Traceable to source inputs

There are **no false positives by design**.

---

## Compliance Alignment

This project aligns with:
- **ALCOA+ data integrity principles**
- **GxP expectations** (GDP / GMP-supporting systems)
- **ICH Q9 risk-based quality management**
- Computer System Validation (CSV)

False negatives are treated as **controlled errors of omission**, not silent failures.

---

## Directory Structure (Conceptual)

```
/Appendix
  /Codes
    /Pre-Phase-A
    /Phase-A
    /Phase-B
    /Phase-C
    /Phase-D
    /Phase-E
```

Each folder contains immutable artifacts and code used for validation and explanation.

---

## Intended Audience

This repository is intended for:
- System engineering review
- Regulatory and compliance discussion
- Interested to know Voice Enabled Features to Products

---

## Final Note

This project demonstrates that **responsible AI system design** in regulated domains requires more than model accuracy. It requires:
- Governance
- Determinism
- Transparency
- Auditability

The pipeline intentionally favors these properties over opaque automation - Not followed Black box concepts

## Project Structure
```
new-p-voice-ai-v3/
│
├── README.md
├── RUN_ALL.txt
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
│
├── Basic_Installation_Guidelines/
│   └── Installations_and_dependencies.txt
│
├── Data_Base/
│   ├── Raw_Audios/
│   │   ├── 1.m4a
│   │   ├── 2.m4a
│   │   ├── ...
│   │   └── 62.mp3
│   │
│   ├── _ground_truth.xlsx
│   └── _master_sheet.xlsx
│
├── execution_controller_agent.py
├── python_main.py
├── runtime_resources.py
├── agent_memory.py
├── agent_reasoner.py
├── agent_state.py
├── agent_transitions.py
│
├── data_pipeline/
│   ├── __init__.py
│
│   ├── audio_quality_matrix.py
│   ├── plot_lufs_quality_corridor.py
│   ├── run_audio_quality_matrix.py
│
│   ├── phase_A_audio_preprocessing.py
│   ├── run_phase_A.py
│
│   ├── phase_B_transcription.py
│   ├── run_phase_B.py
│
│   ├── configs/
│   │   └── audio_preprocess_config.yaml
│
│   ├── utils/
│   │   └── audio_utils.py
│
│   ├── phase_C_structured_boundary_extraction/
│   │   ├── __init__.py
│   │   ├── alias_registry.py
│   │   ├── boundary_rules.py
│   │   ├── extractor.py
│   │   ├── snapshot_loader.py
│   │   └── run_phase_C.py
│
│   ├── phase_D_fuzzy_canonical_mapping/
│   │   ├── __init__.py
│   │   ├── fuzzy_matcher.py
│   │   ├── mapper.py
│   │   ├── master_loader.py
│   │   ├── merge_outputs.py
│   │   ├── text_normalizer.py
│   │   └── run_phase_D.py
│
│   ├── phase_E_evaluation_audit/
│   │   ├── __init__.py
│   │   ├── audit.py
│   │   ├── load_inputs.py
│   │   ├── metrics.py
│   │   └── run_phase_E.py
│
│   └── artifacts/
│       ├── quality_matrix/
│       │   ├── integrated_vs_momentary_lufs_corridor.png
│       │   └── quality_metrics_report_v3.csv
│       │
│       ├── audio_processed/
│       │   ├── 1.wav
│       │   ├── 2.wav
│       │   └── ...
│       │
│       ├── transcripts_raw/
│       │   ├── transcription_1.csv
│       │   └── ...
│       │
│       ├── structured_boundary_extraction/
│       │   ├── phase_C_structured_boundary_consolidated.csv
│       │   └── transcription_*_structured.json
│       │
│       ├── fuzzy_canonical_mapping/
│       │   ├── phase_D_fuzzy_all.csv
│       │   ├── fuzzy_canonical_merged.csv
│       │   └── transcription_*_structured_fuzzy.*
│       │
│       └── evaluation_audit_phase_E/
│           ├── aligned_predictions_vs_gt.csv
│           ├── confusion_matrix.png
│           ├── failure_audit.csv
│           ├── failure_summary.csv
│           ├── metrics.json
│           └── wer_cer_report.csv
│
└── __pycache__/  
```

