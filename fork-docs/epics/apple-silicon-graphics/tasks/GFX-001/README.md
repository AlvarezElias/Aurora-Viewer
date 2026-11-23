# GFX-001: Native MetalFX temporal reconstruction

[Epic](../../README.md) · [Analysis](../../ANALYSIS.md) · [Validation](../../VALIDATION.md)

| Field | Value |
| --- | --- |
| Research | Analysed on 2026-11-22; documented in the fork on 2026-11-23 |
| Implementation | Not started; first task prepared for implementation |
| Target | M3 Max, with runtime OS/device support checks |
| Dependencies | Native texture/command interoperability and existing FSR/TAA inputs |
| Evidence | No local support query, prototype, measurements or human validation |

## Outcome

Offer native MetalFX temporal reconstruction as an optional macOS path and
compare its quality/performance with FSR 3.1. Preserve unsupported-device
fallbacks and existing platform behaviour. This task does not implement
generative relighting, frame generation or a new lighting model.

## Starting points

- [Renderer dependencies](../../../../../crates/aurora-render/Cargo.toml).
- [FSR inputs and host code](../../../../../crates/aurora-render/src/fsr.rs).
- [Motion preparation](../../../../../crates/aurora-render/src/shaders/fsr/prepare_inputs.wgsl).
- [Temporal/postprocessing integration](../../../../../crates/aurora-render/src/renderer.rs).
- [Native Metal precedent](../../../../../crates/aurora-render/src/xr_metal.rs).

Read the relevant source and current ownership again when starting code;
the paths are implementation entry points, not a frozen patch plan.

## First implementation slice

1. Branch from current personal `develop` in an isolated task worktree.
2. Check the exact MetalFX API, OS availability and `supportsDevice` result;
   record unsupported behaviour before enabling any new mode.
3. Prove GPU texture and command interoperability in a bounded demo path,
   with resource lifetime and wgpu usage tracking explicit.
4. Prepare motion format/direction/scale, reverse-Z depth, exposure and jitter.
   Do not pass FSR's exposure or masks through without checking conventions.
5. Insert reconstruction in the temporal stage before postprocessing; avoid
   stacking it on top of FSR/TAA as a second temporal reconstruction.
6. Reset history on first use, camera cuts, teleport/origin shifts, size and
   method changes. Create expensive resources outside the steady frame loop.
7. Expose the option only after the path works; follow shared widgets and
   English/French/Japanese catalogue rules for any viewer text.

Any new module, dependency or launch option updates its corresponding
architecture, notices or testing documentation in the implementation change.

## Acceptance checklist

- [ ] Device support and initialization/refusal/fallback behaviour recorded.
- [ ] No production per-frame CPU image readback or synchronous GPU wait.
- [ ] Native, FSR 3.1 and MetalFX compared at equal internal/output sizes.
- [ ] GPU cost, memory and frame-time variation measured on the M3 Max.
- [ ] Motion, disocclusion, animated textures and reactive effects checked.
- [ ] Hair, water, glass, particles, emissives and fine geometry reviewed.
- [ ] UI/HUDs, depth-dependent effects, selection and photos remain correct.
- [ ] Appropriate checks/CI and demo comparisons pass; limits recorded.
- [ ] Human accepts the image and smoothness before an upstream PR.

## Decision gate

Advance only if equivalent comparisons show a useful quality or performance
benefit without material regressions. Otherwise record the result and retain
the existing rendering choice. A support-table entry is not an acceptance test.

## Sources

- [Apple: temporal scaler descriptor](https://developer.apple.com/documentation/metalfx/mtlfxtemporalscalerdescriptor)
- [Apple: MetalFX integration and reactive masks](https://developer.apple.com/videos/play/wwdc2025/211/)
- [Apple: GPU feature tables](https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf)
- [Rust bindings reviewed during research](https://docs.rs/objc2-metal-fx/0.3.2/objc2_metal_fx/)
