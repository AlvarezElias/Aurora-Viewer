# Decisions and open questions

[Epic](README.md) · [Analysis](ANALYSIS.md)

## Recorded decisions

| Date | Decision | Scope |
| --- | --- | --- |
| 2026-11-22 | Preserve native MetalFX and experimental generative research as separate tracks | Research; no runtime implementation or local measurements |
| 2026-11-23 | Store an English epic and GFX task folders in the personal fork, on a branch from `develop`, then integrate the documentation into `develop` | Explicit documentation/integration request; no upstream PR |
| 2026-11-23 | Prepare GFX-001 as the first implementation handoff | Planning sequence; all renderer tasks remain not started |

The original conversation placed particular value on generative changes to
lighting, skin and materials. Starting with GFX-001 provides a bounded native
integration step; it does not claim that temporal reconstruction delivers
that generative effect or that GFX-004 has become unnecessary.

## Proposed design, not yet implemented

- Use a small macOS-only interoperability layer while retaining existing
  platform paths and fallback behaviour.
- Keep production frame data on the GPU, without per-frame CPU image
  readbacks or synchronous GPU waits.
- Compare native resolution, FSR 3.1 and MetalFX with equivalent workloads.
- Keep UI, cursor, names and HUD composition explicit for interpolation and
  generative processing.
- Treat denoising as dependent on a specific source effect, not a standalone
  global-illumination feature.
- Begin generative evaluation with synthetic demo images before live sessions.

## Open before choosing a runtime implementation

1. **Native interoperability:** can the exact wgpu/Metal versions share
   textures and ordered commands with all required usage and lifetime rules?
2. **Quality and budget:** which modes actually improve the M3 Max result,
   and what are their complete GPU, memory and latency costs?
3. **Product claims:** official downloads currently promise no AI feature or
   model in [README.md](../../../README.md). Any neural feature proposed for
   the fork must have its scope, disclosure and branding decided explicitly;
   this documentation does not change the upstream policy or distribution.
   Evaluate native framework usage separately from bundling third-party models.
4. **Dependencies and models:** source-code licences do not grant rights to
   redistribute extracted NVIDIA weights. There is no approved dependency or
   model-distribution choice yet.
5. **Creator permissions:** preserve existing permission helpers for assets,
   IDs, snapshots and exports; do not make the research a route around them.
6. **Shared-world behaviour:** enhancement is local display work. Never store
   Aurora-only metadata in assets, object fields, names, chat or other shared
   server data, and do not introduce viewer-specific signalling.
7. **Contributor overlap:** check current fork/upstream issues, PRs and work
   ownership before starting code. The documentation transfer did not verify
   that inventory because `gh` was unavailable.

Recording a question is not a decision to implement its most permissive
answer. A later task records the chosen option, evidence and validation here
and in its task folder, keeping the history visible.

## Progress log

- **2026-11-22:** initial source review and personal Spanish Markdown/HTML
  tracker. No model execution or renderer changes.
- **2026-11-23:** transfer into an English, fork-only epic with four task
  folders and a common validation plan. Renderer code, dependencies and
  runtime settings remain unchanged. Documentation integration is not runtime
  validation.
- **2026-11-23 documentation checks:** nine Markdown documents and 53 local
  references/anchors checked, with task IDs and unchecked runtime acceptance
  gates verified. `git diff --check` passed. Full `check.ps1` could not start
  because `pwsh` is not installed; no Rust compilation, GPU test or CI result
  is claimed for this documentation-only change. No upstream synchronization
  is part of this task; `origin/develop` was fetched before branching.
