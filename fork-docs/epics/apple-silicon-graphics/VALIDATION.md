# Shared validation plan

[Epic](README.md) · [Tasks](README.md#tasks)

## Evidence available now

Only source review and external reports. There are no local MetalFX support
results, model outputs, M3 Max performance measurements, demo captures or
human acceptance records for these proposed features. Documentation checks
must not be reported as renderer tests.

## Reproducible experiment record

Keep a dated Markdown record in the relevant GFX task folder. Record:

- Source commit, task branch, dependency/model version and test command.
- Exact GPU configuration, memory, OS, toolchain, power mode and other GPU load.
- Demo scenario, camera, input/output resolution and graphics options.
- Warmup, sample count, run order and the method used to collect timings.
- Native/FSR/MetalFX or effect-off/on baselines with equivalent workloads.
- Real rendered FPS and presented FPS separately; GPU time, frame-time
  variation, memory and latency when a documented measurement method exists.
- Expected and observed images, artefacts and failure/fallback behaviour.
- What the human tested, when, and whether the result was accepted.

Do not create empty result tables that look like completed benchmarks. Store
temporary captures and logs in the task's ignored `.scratch/` folder; reference
sanitized evidence through the repository's supported capture workflow when
publishing a PR. Do not commit models, binary dumps, personal paths or grid data.

## Demo and quality matrix

Compare still and moving cameras, camera cuts, resolution changes, avatar
motion/deformation, hair, patterned clothing, signs, thin geometry, glass,
water, particles, emissives, changing lighting and arriving assets. Check
selection, HUDs, names, UI sharpness, snapshots and any neighbouring effects
whose inputs or ordering change. Both interface layouts must retain their
behaviour when a task exposes settings or controls.

Generative comparisons also check identity changes, invented text/detail,
material changes and flicker. Denoising comparisons require a defined noisy
source effect and, where feasible, a higher-sample reference image.

## Execution rules

Follow [AGENTS.md](../../../AGENTS.md),
[FORK_WORKFLOW.md](../../../FORK_WORKFLOW.md) and
[TESTING.md](../../../docs/TESTING.md). Work in the task's own worktree and
default target directory. Respect the pinned toolchain, build slots and
applicable platform CI; do not bypass them to obtain a prototype.

Use per-launch `AURORA_*` options or command-line arguments for tests. Never
edit the shared settings file or change Preferences to prepare an automated
measurement. Check the log for the effective test settings; report unexpected
values rather than overwriting them. If a required launch-only option does
not exist, add and document it in the implementation task or ask the human.

Offline runs use the required `Test <task>` title and the automation marker
when driven automatically. Agents never connect to a grid or handle login
credentials. If grid validation becomes necessary, launch the appropriate
viewer and give the human precise steps; they log in and test.

## Gates

1. **Prototype:** device checks and failure handling work; there is a bounded
   executable experiment with its limitations recorded.
2. **Measured:** reproducible local evidence shows benefit or a reason to stop.
3. **Human validated:** visual behaviour and usability are explicitly accepted.
4. **Personally integrated:** authorized merge to `develop` preserves its old
   history and the task commit. Pending checks remain visible in `TASKS.md`.
5. **Upstream proposal, if requested:** independent branch, no personal fork
   documents/features bundled, and the separate upstream review/CI process.

A task can be measured and rejected. Keep that result; do not silently relabel
the research as successful because documentation or prototype code merged.
