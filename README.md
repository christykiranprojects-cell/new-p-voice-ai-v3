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

This project follows a **system-engineering-first approach**, not a pure end-to-end AI approach.

Core principles:
- **Control Plane ≠ Data Plane** separation
- Heavy AI workloads are **explicitly governed**, not implicitly executed
- Errors are **measured and logged**, not hidden
- Quantity correctness is treated as a **protected invariant**

In regulated pharmaceutical workflows, **traceability and safety are prioritized over raw automation accuracy**.

---

## High-Level Architecture

The pipeline is organized into clearly defined phases:

```
Pre-Phase A → Phase A → Phase B → Phase C → Phase D → Phase E
   (Assess)    (Audio)   (ASR)     (Rules)    (Fuzzy)   (Audit)
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

## Pre-Phase A — Audio Quality Assessment (Quality Matrix)

A **read-only assessment layer** that evaluates audio *before* any preprocessing.

Metrics include:
- Integrated LUFS
- Momentary LUFS
- Silence ratio
- Residual DC offset
- Duration and channel count

Outputs:
- `quality_metrics_report.csv`
- LUFS corridor visualization

This layer ensures evaluation validity by separating **measurement** from **transformation**.

---

## Phase A — Audio Preprocessing

Deterministic signal processing to produce a canonical audio format:
- 16 kHz sampling
- Mono channel
- 16-bit PCM WAV

Operations include:
- DC offset removal
- Loudness normalization
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
- Model loading only in `ACT` state
- CPU threads governed by agent
- Transcription outputs are immutable

This phase converts normalized audio into **raw transcription artifacts**.

---

## Phase C — Structured Boundary Extraction

A **rule-based NLP layer** that converts raw text into structured medicine items.

Features:
- Deterministic BEGIN–MID–END boundary logic
- Frozen medicine-type alias registry
- Explicit quantity extraction

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
- Academic evaluation (MCA / M.Tech projects)
- System engineering review
- Regulatory and compliance discussion

---

## Final Note

This project demonstrates that **responsible AI system design** in regulated domains requires more than model accuracy. It requires:
- Governance
- Determinism
- Transparency
- Auditability

The pipeline intentionally favors these properties over opaque automation - Not followed Black box concepts

