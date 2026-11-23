---
name: aurora-gfx-validation
description: "Plan or record reproducible Aurora graphics experiments, before/after evidence and human acceptance. Use for an explicit rendering comparison, benchmark or visual validation task; not for routine documentation checks or automatic grid testing."
---

# Aurora graphics validation

Read the active repository's AGENTS.md, FORK_WORKFLOW.md and the relevant
GFX task plus its shared VALIDATION.md. Use current docs/TESTING.md for actual
launch options. The task decides what hypothesis is being tested; the skill
does not authorize implementing other wishlist ideas.

## Plan before consuming the GPU

Run `python3 scripts/fork-tracker.py status` to identify the checkout, local
changes, platform and available tools. Check the pinned toolchain and build
gate requirements without downloading or changing them merely for inventory.
Follow AGENTS.md's platform/build policy; do not invent a workaround for an
unavailable Windows or CI check on macOS. Record the limitation.

Define equivalent baseline/candidate workloads, fixed internal and output
resolution, exact demo scene/camera, warmup, sampling method and run order.
Keep real rendered FPS separate from presented/interpolated FPS. Do not infer
latency from either counter. Compare nearby runs with equivalent GPU load.

## Execute only the authorized experiment

- Use the task's own worktree/default target and required window title.
- Test offline with per-launch options. Never prepare an experiment by
  changing shared Preferences/settings, reading the cache outside viewer
  helpers, logging into a grid or handling credentials.
- Use the existing profiler and capture mechanisms. Keep expensive image
  processing and production per-frame CPU readbacks/blocking GPU waits out
  of the render path; measure any interoperability cost explicitly.
- Visually inspect actual before/after captures, including neighbouring
  features and both UI styles where affected. Preserve creator permissions
  and do not send renderer-specific data through shared world fields.
- A human performs any required grid test and the final viewer acceptance.
  Personal develop integration alone does not close those gates.

## Record a result, including an unsuccessful one

Use [the measurement template](assets/measurement.md) in the task folder.
Replace fields with actual observations; record unavailable measurements as
unavailable, not zero. Store temporary raw logs/captures in ignored scratch
and reference sanitized evidence through the repository's supported workflow.
Only advance task metadata when a corresponding evidence record exists.
Use fork-docs/TRACKER.md for the evidence and stage fields; synchronize the
task's TASKS.md entry without rewriting another task.

Run the tracker validator and refresh the presentation after a recorded
result. Report what was tested, the practical limits, human acceptance status
and the next decision. Do not automatically publish or merge from a benchmark
request.
