# GFX-003: Neural denoising for lighting

[Epic](../../README.md) · [Analysis](../../ANALYSIS.md) · [Validation](../../VALIDATION.md)

| Field | Value |
| --- | --- |
| Research | Analysed on 2026-11-22; documented in the fork on 2026-11-23 |
| Implementation | Not started; exploratory and conditional |
| Dependency | A selected noisy lighting/reflection effect and suitable auxiliary buffers |
| Evidence | No source-effect prototype, denoiser execution or local comparison |

## Outcome

Evaluate whether MetalFX denoising can make a specific low-sample lighting
or reflection effect useful at an interactive budget. Adding a denoiser to
today's final raster image does not itself add ray tracing, global illumination
or DLSS-style generative materials.

## Design to investigate

Choose a bounded source effect before committing to a new path tracer.
Define its noise characteristics, reference image and budget. Establish
noise-free normal, diffuse/specular albedo and roughness buffers alongside
colour, depth and motion. Check conventions and texture formats explicitly.

Consider optional specular hit distance, denoising strength and transparency
overlay inputs. Mirrors and glass may need auxiliary properties representing
the reflected/transmitted surface. Sky and already-clean effects should not
be denoised indiscriminately. Review the fork/official product scope in the
[decision log](../../DECISIONS.md) before a neural feature enters a build.

## Acceptance checklist

- [ ] A real source effect, its budget and need for denoising defined.
- [ ] OS/device support and fallback verified.
- [ ] Auxiliary inputs inspected through debug views.
- [ ] Low-sample raw, denoised and feasible higher-sample reference compared.
- [ ] Noise reduction, lost detail, motion stability and GPU/memory cost measured.
- [ ] Reflections, glass, emissives, disocclusions and avatars checked.
- [ ] Relevant dependencies, notices, checks and human acceptance recorded.

## Decision gate

Continue only if a concrete effect improves the viewer's appearance within
a viable budget. Until a source effect exists, this remains research rather
than a ready implementation task.

## Sources

- [Apple: denoised scaler descriptor](https://developer.apple.com/documentation/metalfx/mtlfxtemporaldenoisedscalerdescriptor)
- [Apple: auxiliary inputs and denoising](https://developer.apple.com/videos/play/wwdc2025/211/)
- [Apple: neural rendering integration](https://developer.apple.com/videos/play/wwdc2026/359/)
