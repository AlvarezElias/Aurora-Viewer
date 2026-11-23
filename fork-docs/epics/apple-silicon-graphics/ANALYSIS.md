# Graphics research: findings and sources

[Epic](README.md) · [Validation plan](VALIDATION.md)

Initial external-source review: **2026-11-22**. Transferred into the fork:
**2026-11-23**. This transfer preserves the analysis; it is not a new runtime
test or a fresh verification of every external project.

## Different techniques solve different problems

| Technique | Intended benefit | What it does not establish |
| --- | --- | --- |
| Temporal reconstruction | Reconstruct a sharper, steadier output from a smaller rendered image | A performance or quality win over Aurora's FSR without a comparison |
| Frame interpolation | Insert intermediate images for smoother presentation | Faster simulation, network updates or input response |
| Neural denoising | Reconstruct noisy lighting/reflection signals from fewer samples | Global illumination or ray tracing without implementing the source effect |
| Generative image enhancement | Change the apparent lighting, materials and detail of rendered pixels | Higher-resolution original assets, physically correct lighting or unchanged identities/text |

MetalFX provides native APIs for the first three areas. It is not a ready-made
equivalent of DLSS 5 generative appearance enhancement. Apple also exposes
tools for custom neural rendering, but adopting them still requires a suitable
model, training or conversion work, integration and performance evidence.
See [Apple's MetalFX overview](https://developer.apple.com/documentation/metalfx)
and [neural rendering discussion](https://developer.apple.com/videos/play/wwdc2026/359/).

## Aurora baseline

The original analysis examined official baseline `d10b1f683`. The documentation
branch starts from personal `develop` at `3aee157056eabfe2c26473cdb67b6b7e1f59ae25`;
its renderer dependencies and relevant source paths were checked again during
this transfer. Neither review proves runtime compatibility.

- [Renderer dependencies](../../../crates/aurora-render/Cargo.toml): wgpu
  30.0.1, objc2 and objc2-metal. macOS uses Metal rather than a Vulkan
  translation layer.
- [FSR host code](../../../crates/aurora-render/src/fsr.rs): FSR 3.1 already
  consumes HDR colour, reverse-Z depth, jitter and motion before tone mapping.
- [FSR input preparation](../../../crates/aurora-render/src/shaders/fsr/prepare_inputs.wgsl):
  motion is read from `zw`, with camera reprojection where the prepass supplies
  none. A different consumer needs an explicit format, direction and scale
  conversion rather than the assumption that these inputs are interchangeable.
- [Renderer](../../../crates/aurora-render/src/renderer.rs): FSR replaces
  the TAA step; downstream passes work from its reconstructed image/depth.
- [Metal interoperability](../../../crates/aurora-render/src/xr_metal.rs):
  the existing XR path accesses the native queue and imports native textures.
  This is useful precedent, not a completed MetalFX bridge.
- [Task tracking](../../../TASKS.md): FSR 3.1 is present; Frame Generation
  is still recorded as future investigation. No MetalFX integration was
  identified in the renderer reviewed for this epic.

The original environment reported macOS 26.6.2 and Xcode 27.2. No MetalFX
`supportsDevice` check, model inference or M3 Max benchmark was run. Record
the actual OS, toolchain and GPU configuration when executing each experiment.
GitHub issue and PR inventory was not checked with `gh`, which was unavailable;
do not infer that no contributor is working on these areas.

## Native MetalFX feasibility

Apple's [feature tables](https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf)
include the M3 family for the capabilities under discussion. The
[temporal scaler](https://developer.apple.com/documentation/metalfx/mtlfxtemporalscalerdescriptor)
is available from macOS 13; the
[frame interpolator](https://developer.apple.com/documentation/metalfx/mtlfxframeinterpolatordescriptor)
and [denoised scaler](https://developer.apple.com/documentation/metalfx/mtlfxtemporaldenoisedscalerdescriptor)
are documented from macOS 26. Check OS availability and each descriptor's
device-support query at runtime; the hardware name alone is not the gate.

The proposed bridge uses existing GPU textures and ordered GPU submissions.
Evaluate the [Rust MetalFX bindings](https://docs.rs/objc2-metal-fx/0.3.2/objc2_metal_fx/)
and wgpu's native encoder access against the exact version in the task.
The prototype must prove resource lifetime, usage tracking and synchronization;
an Objective-C binding does not by itself solve these constraints.

Place temporal reconstruction before postprocessing. Validate exposure,
reverse-Z, unjittered motion, texture formats, camera cuts and resolution
changes. Do not reuse an FSR-tuned reactive mask without evaluating it for
MetalFX. Place interpolation after tone mapping and design the composition
and pacing of original/intermediate frames. For denoising, first identify a
real source effect and its noise-free auxiliary buffers. These integration
principles follow [Apple's MetalFX session](https://developer.apple.com/videos/play/wwdc2025/211/).

## Experimental generative routes

Lack of official NVIDIA support for an Apple GPU does not rule out a separate
inference implementation. The initial search found:

- [MLX-DLSS](https://github.com/iamwavecut/MLX-DLSS): an experimental port
  with MLX/Metal and Core ML paths plus library APIs. Its author explicitly
  distinguishes it from an integrated game or an NVIDIA product.
- [dlss5-macos-overlay](https://github.com/gtrg55/dlss5-macos-overlay): an
  external capture/processing/overlay application based on MLX-DLSS. Its
  [architecture](https://github.com/gtrg55/dlss5-macos-overlay/blob/main/docs/ARCHITECTURE.md)
  includes reduced-resolution processing and inferred motion, with additional
  capture/presentation considerations.
- [DLSS-NR-on-AMD](https://github.com/danielblnc/DLSS-NR-on-AMD): a Windows
  DirectX 12 adaptation. It demonstrates a separate portability effort;
  its runtime and measurements are not a macOS solution.

The Mac approach processes model data with an Apple-compatible backend; it
does not execute a Windows NVIDIA DLL directly. No complete NVIDIA-runtime
parity or direct wgpu integration has been established here. The
[NVIDIA announcement](https://www.nvidia.com/en-us/geforce/news/dlss-5-3d-guided-neural-rendering/)
consulted on 2026-11-22 described a September 2026 launch; release status is
separate from official Apple GPU support and should be rechecked before use.

## External performance evidence

These are project authors' reported results, not measurements of this fork.

| Project / device | Workload | Reported result | Exclusion |
| --- | --- | --- | --- |
| MLX-DLSS / M2 Max | Small network, warm 1088 × 1920 extent | About 64.6–65.6 ms per network evaluation | Not Aurora's full frame or an M3 Max result |
| MLX-DLSS / M2 Max | Temporal 1080p video, 60 input frames | 5.91–6.05 seconds | Not interactive 60 FPS |
| Overlay / M4 Max | Synthetic 960 × 540 pattern reduced to 512 × 288 | 29.98 ms; 33.36 processed frames/s after warmup | Capture and display excluded; not full-resolution game inference |

Sources: [MLX-DLSS integration and measurements](https://github.com/iamwavecut/MLX-DLSS/blob/main/docs/embedding.md#performance),
[overlay validation](https://github.com/gtrg55/dlss5-macos-overlay/blob/main/docs/VALIDATION.md).
Different versions, workloads and devices make these unsuitable for a
chip-to-chip comparison. A complete 60 FPS frame has approximately 16.7 ms;
the model would also compete with Aurora for GPU time and memory.

## Integration and distribution limits

Start GFX-004 with synthetic demo images, then test motion sequences only
if the image effect is useful. Direct texture interoperability might remove
some capture overhead, but that is a hypothesis requiring its own prototype.
Do not assume that lower processing resolution or skipping alternate frames
preserves detail and temporal consistency.

MLX-DLSS identifies its source as Apache-2.0; the overlay identifies its own
code as MIT and the vendored component separately. The model data is not
covered by those source licences. Upstream says extracted models retain the
vendor's terms and must not be redistributed. This epic includes no weights,
runtime binaries or approved model-distribution plan. Recheck those conditions
and Aurora's dependency rules before incorporating anything.

The current [README](../../../README.md) also describes official downloads
as having no AI feature or model. This research is a personal-fork proposal,
not a change to that official policy. See [DECISIONS.md](DECISIONS.md) for
the unresolved scope and distribution questions before runtime work.
