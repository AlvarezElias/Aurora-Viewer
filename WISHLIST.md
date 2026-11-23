# Aurora Viewer wishlist

Desired features and investigation ideas for the personal fork. This is
planning context, not an instruction to implement every entry. Active work,
integrated features and validation status are tracked in [TASKS.md](TASKS.md).
Agents must follow [FORK_WORKFLOW.md](FORK_WORKFLOW.md) for branch management
and personal integration.

## Apple Silicon graphics

Investigate native MetalFX reconstruction and interpolation on the M3 Max,
conditional neural denoising for a defined lighting effect, and experimental
generative image enhancement. The latter is the main visual interest;
MetalFX reconstruction alone does not provide it.

The [GFX epic](fork-docs/epics/apple-silicon-graphics/README.md) contains the
analysis, decisions, shared validation plan and separate GFX-001 through
GFX-004 folders. GFX-001 is the first prepared implementation task. All four
remain research only: no prototype, local benchmark or human validation.
The epic records the official no-AI product claim and unresolved model-use
and distribution questions before a runtime feature is chosen.

## Tabbed viewer sessions

Open independent viewer sessions as tabs. Reorder tabs by dragging, detach a
tab to its own window, and move it back into a tab group. Moving a tab should
keep its login, world state, chat history and camera. Each session can use
the current profile or a named profile, independently of where it appears.

### Background tabs

A hidden tab should stay connected and receive chats, IMs and notifications
while doing as little work as possible. Keep enough world state for a fast
return without logging in again. Stop drawing the hidden tab's 3D world and
update its tab badge and notifications as messages arrive. If the session
is detached and visible, use the existing background-window rules when it
loses focus.

Aurora already limits the work of background windows. The
[instance tracker](crates/aurora-viewer/src/instances.rs) caps a background
viewer at 10 FPS when another viewer is in front on the same GPU and the
background cap is enabled. The
[busy GPU pause](crates/aurora-viewer/src/app/busy_pause.rs) can suspend 3D
drawing while chat, networking, sound and the interface continue. It keeps
textures resident for a quick return when GPU time is the constraint.
The [texture budget](crates/aurora-viewer/src/scene/texture_budget.rs)
can give memory back under pressure. A hidden tab could use its visibility
to trigger the pause, with a separate decision about when to release memory.

### To investigate

- Separate session lifetime from the render surface so a tab can move
  between windows without reconnecting or losing focus and input state.
- Determine which network events, chat and notification updates need a prompt
  wake-up and which world updates, asset uploads or media work can slow down.
- Compare keeping render resources warm with releasing large render targets
  first and evicting textures only under memory pressure. Check both fast
  switching and prolonged periods in the background.
- Measure CPU and GPU use, RAM and VRAM, notification delay, and time to the
  first usable frame after switching or detaching. Use two equivalent demo
  sessions and compare hidden tabs with two separate viewer windows.
