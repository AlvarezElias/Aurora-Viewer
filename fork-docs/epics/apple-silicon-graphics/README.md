# Epic: Apple Silicon graphics

| Field | Status |
| --- | --- |
| Epic ID | GFX |
| Target hardware | M3 Max; measure the exact configuration before drawing conclusions |
| Initial research | 2026-11-22 |
| Fork documentation | 2026-11-23 |
| Research maturity | Initial analysis recorded; external claims require rechecking before implementation |
| Runtime maturity | No prototype, local benchmark or human validation |
| First implementation task | GFX-001 |

## Purpose

Investigate native reconstruction and smoother presentation on Apple Silicon,
alongside experimental changes to the appearance of lighting and materials.
Generative image enhancement remains the human's main visual interest.
Start implementation planning with GFX-001, the first numbered task, while
keeping the other tracks explicit rather than implying that MetalFX supplies
generative relighting.

This epic records research and a proposed implementation sequence. The
current request authorizes documentation and personal `develop` integration;
it does not start the renderer implementation or install third-party models.

## Tasks

| ID | Task | Research | Implementation | Dependency / next gate |
| --- | --- | --- | --- | --- |
| [GFX-001](tasks/GFX-001/README.md) | Native MetalFX temporal reconstruction | Analysed | Not started | Verify device support and GPU interoperability; compare with FSR 3.1 |
| [GFX-002](tasks/GFX-002/README.md) | Native frame interpolation | Analysed | Not started | Reuse GFX-001 input/interoperability work; design UI composition and frame pacing |
| [GFX-003](tasks/GFX-003/README.md) | Neural denoising for lighting | Analysed | Not started | Select a noisy lighting/reflection effect and define its auxiliary buffers |
| [GFX-004](tasks/GFX-004/README.md) | Generative image enhancement | Analysed | Not started | Check model conditions and compare offline demo images before considering live integration |

GFX-003 and GFX-004 are distinct research tracks, not automatic successors to
frame interpolation. Their additional prerequisites may keep them at the
research stage even if GFX-001 and GFX-002 succeed.

## Shared documents

- [Analysis and sources](ANALYSIS.md): rendering baseline, API scope,
  experimental ports and external measurements.
- [Decisions and open questions](DECISIONS.md): accepted documentation scope,
  proposed runtime design and unresolved policy/model questions.
- [Validation plan](VALIDATION.md): reproducible comparisons, evidence format
  and human acceptance gates.

## Definition of success

Each implemented option demonstrates a useful visual or performance benefit
against an equivalent baseline and remains optional. Unsupported configurations
retain their existing path. GPU work stays on the GPU, input and simulation
remain responsive, and permissions and shared-world behaviour stay intact.

Record failed experiments as well as successful ones. Do not promise higher
FPS, more realistic lighting or parity with NVIDIA from API availability or
results measured by another project on another chip.

## Scope boundaries

These are personal-fork proposals, not an upstream roadmap or an official
download feature claim. No assets, models, renderer code, settings, network
protocols, dependencies or CI configuration are changed by this epic's
documentation commit. See [the decision log](DECISIONS.md) before moving from
research to an experimental build.
