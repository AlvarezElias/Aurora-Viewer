---
id: "GFX-002"
title: "Native frame interpolation"
area: "Smoothness"
stage: "analysed"
interest: "Medium"
researched: "2026-11-22"
updated: "2026-11-23"
summary: "Generate intermediate images while keeping rendered and presented FPS distinct."
next_step: "Build on GFX-001 input work and define UI composition, pacing and latency measurements."
evidence: ""
---

# GFX-002: Native frame interpolation

[Epic](../../README.md) · [Analysis](../../ANALYSIS.md) · [Validation](../../VALIDATION.md)

| Field | Value |
| --- | --- |
| Dependency | GFX-001 interoperability/input work; composition and pacing design |
| Evidence | No interpolator execution, timing measurements or human validation |

## Outcome

Generate intermediate images with MetalFX for smoother presentation. Do not
equate presented FPS with rendered FPS, simulation speed or control response.
Provide an explicit off switch and preserve the original presentation path.

## Design to investigate

Use consecutive rendered images, depth and correctly scaled motion. Place
interpolation after tone mapping. Decide how UI, cursor, nameplates, labels,
selection tools and HUDs are composed so text does not inherit world-motion
distortion. Record whether UI is separate, composited or drawn every frame.

Frame production and presentation must remain ordered and evenly paced.
Define resource reuse, dropped frames, reset boundaries, FPS caps, vsync,
minimization, resizing and display changes. Sharing GFX-001 inputs does not
require adopting its reconstruction mode for every interpolation configuration.

## Acceptance checklist

- [ ] OS/device support and unsupported fallback verified.
- [ ] Composition policy demonstrated with readable UI, names and HUDs.
- [ ] Original and interpolated frames presented at the intended cadence.
- [ ] Rendered/presented FPS reported separately at equivalent source FPS.
- [ ] GPU cost, memory, frame-time variation and a documented latency method recorded.
- [ ] Rapid camera motion, disocclusions, thin geometry and transparency checked.
- [ ] Caps, vsync, dropped frames and reset/resize behaviour checked.
- [ ] No production blocking GPU waits or main-thread heavy work introduced.
- [ ] Appropriate checks and human acceptance recorded.

## Decision gate

Retain the option only for configurations where measured pacing and human
assessment show useful smoothness with acceptable latency and artefacts.
FPS multiplication alone is not the acceptance criterion.

## Sources

- [Apple: frame interpolator descriptor](https://developer.apple.com/documentation/metalfx/mtlfxframeinterpolatordescriptor)
- [Apple: composition and frame pacing](https://developer.apple.com/videos/play/wwdc2025/211/)
- [Apple: GPU feature tables](https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf)
