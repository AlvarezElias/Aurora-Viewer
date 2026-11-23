# Aurora Viewer wishlist

Ideas for future work on the fork's `develop` branch.

## Fork branch workflow

- `main` mirrors the official repository's `main`. Update it by fast-forward
  only and keep personal features out of it.
- `develop` combines the official baseline with the fork's personal features.
  Build this branch to use those features together, even while upstream pull
  requests are awaiting review.
- Keep each feature on its own branch based on official `main`. Merge it into
  `develop` when it is ready for personal integration; submit upstream pull
  requests from the feature branch, so the fork's other changes stay separate.

Bring official updates into `main` first, then merge `main` into `develop`,
resolving conflicts while retaining the personal features. Each branch has
its own worktree. Keep unfinished work on its feature branch until it is ready
to integrate. Merging into `develop` does not imply upstream acceptance,
human validation, or inclusion in an official release.

### Included in the personal branch

- Quick lens presets in Camera Controls: 24, 35, 50, 85 and 135 mm, plus
  reset, in both layouts and the free-camera tab. Integrated on 2026-11-23;
  [upstream PR #3730](https://github.com/Aurora-Viewer/Aurora-Viewer/pull/3730)
  remains separate. Integrated runtime checks and human validation are pending.

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
