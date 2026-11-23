---
id: "GFX-004"
title: "Generative image enhancement"
area: "Neural rendering"
stage: "analysed"
interest: "Primary"
researched: "2026-11-22"
updated: "2026-11-23"
summary: "Explore changes to apparent lighting, skin, materials and detail."
next_step: "Check permitted model use and compare synthetic demo images with local M3 Max measurements."
evidence: ""
---

# GFX-004: Generative image enhancement

[Epic](../../README.md) · [Analysis](../../ANALYSIS.md) · [Validation](../../VALIDATION.md)

| Field | Value |
| --- | --- |
| Dependency | Suitable model/backend, permitted use, product scope and an offline comparison |
| Evidence | External reports only; no local inference or M3 Max measurements |

## Outcome

Evaluate neural changes to apparent lighting, skin, materials and fine detail.
Preserve an immediate original/result comparison and an off switch. The effect
changes displayed pixels; it does not recover original high-resolution assets
or guarantee physically correct lighting, identity or text.

## Candidates and limits

The [shared analysis](../../ANALYSIS.md#experimental-generative-routes)
records MLX-DLSS, its macOS overlay consumer and a separate Windows AMD port.
Apple-compatible inference is possible to investigate; a Windows DLL is not
directly executable on the Mac GPU. These projects do not establish an
integrated, temporally stable, interactive renderer on the M3 Max.

The [external measurements](../../ANALYSIS.md#external-performance-evidence)
include roughly 65 ms per small-network 1080p evaluation on an M2 Max and
reduced-resolution overlay results on an M4 Max. Treat them as cost warnings
for experiment design, not predicted M3 Max FPS. Recheck current versions
and the projects' fidelity limits before selecting a candidate.

## First experiment

1. Resolve the model's allowed use and keep proprietary data outside Git.
   No source-code licence alone authorizes redistributing model weights.
2. Use synthetic offline demo images covering skin, hair, reflective materials,
   indoor/outdoor light, signs and patterned clothing.
3. Compare originals and results with exact model settings, runtime/memory
   measurements and unwanted changes recorded.
4. If the image change is useful, test sequences for flicker, identity/text
   changes and temporal stability before considering a live engine bridge.

Do not start by installing an external capture tool into the viewer or
bundling a model. Production texture interoperability and synchronization
need their own prototype. A direct engine bridge might save capture work,
but the inference budget still competes with rendering.

## Later integration questions

Keep UI, cursor, names and HUDs outside generative processing where appropriate.
Determine colour-space/HDR handling and ordering relative to tone mapping and
upscaling from the model's actual contract. Lower resolution or less frequent
inference can lose detail or consistency; skipping frames is not automatically
a valid optimization. Preserve creator permissions and keep all enhancement
local, without Aurora-only shared metadata or signalling.

## Acceptance checklist

- [ ] Permitted model use, dependency conditions and fork product scope resolved.
- [ ] Original/result demo comparisons and local M3 Max timings recorded.
- [ ] Identity, lettering, patterns and material fidelity evaluated.
- [ ] Motion sequences checked for flicker and coherence.
- [ ] Memory and GPU contention measured with Aurora rendering concurrently.
- [ ] HDR, UI, snapshots, exports and asset permissions handled explicitly.
- [ ] No claim of NVIDIA-runtime parity without a matching comparison.
- [ ] Appropriate checks and human acceptance recorded before integration.

## Decision gate

A useful visual change and viable complete cost must both be demonstrated.
An offline-only result is a valid research outcome; it does not automatically
justify a live viewer option. The official no-AI product claim and model
distribution remain open in [DECISIONS.md](../../DECISIONS.md).

## Sources

- [MLX-DLSS](https://github.com/iamwavecut/MLX-DLSS)
- [Embedding and measurements](https://github.com/iamwavecut/MLX-DLSS/blob/main/docs/embedding.md)
- [Recovery and fidelity limits](https://github.com/iamwavecut/MLX-DLSS/blob/main/docs/recovery-notes.md)
- [macOS overlay](https://github.com/gtrg55/dlss5-macos-overlay)
- [Overlay validation](https://github.com/gtrg55/dlss5-macos-overlay/blob/main/docs/VALIDATION.md)
- [Separate AMD port](https://github.com/danielblnc/DLSS-NR-on-AMD)
- [NVIDIA research](https://research.nvidia.com/labs/adlr/DLSS5/)
