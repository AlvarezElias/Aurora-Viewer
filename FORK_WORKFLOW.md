# Personal fork workflow — instructions for agents

Read this file at the start of every session, together with
[AGENTS.md](AGENTS.md), [ARCHITECTURE.md](ARCHITECTURE.md),
[TASKS.md](TASKS.md) and [WISHLIST.md](WISHLIST.md). Follow it whenever
working on this fork. It defines Git destinations and the personal workflow;
AGENTS.md still governs safety, asset permissions, licensing, translations,
code quality, testing and human validation. A later explicit instruction
from the human takes precedence.

## Repository and branch roles

- `upstream` is the official repository, `Aurora-Viewer/Aurora-Viewer`.
- `origin` is the personal fork, `AlvarezElias/Aurora-Viewer`.
- `main` is a clean mirror of official `main`. Keep personal features,
  wishlist changes and fork-specific instructions out of it. Update it by
  fast-forward only. Never resolve divergence by resetting or force-pushing
  it without the human's explicit instruction.
- `develop` is the personal integration branch. It combines the current
  official baseline with the human's features. Use it for personal builds
  that need those features together. Preserve its published history: merge
  updates instead of rebasing or replacing the branch.
- Each feature has its own branch and worktree. For a feature intended for
  upstream, start from current official `main`, keeping its changes separate
  from the other personal features.

Before any Git operation, check the actual branch, worktree, remotes, local
edits and remote references. Do not assume that `origin` is the official
repository, or that a worktree's folder name identifies its active branch.
Reuse a suitable task-owned worktree and preserve other agents' work.

## Integrating a personal feature

1. Work on the feature's isolated branch, following AGENTS.md. Keep its
   implementation, translations, documentation and validation together.
2. When the human authorizes personal integration, merge that feature into
   `develop`. Upstream acceptance is not a prerequisite. Keep incomplete
   checks and human validation explicitly pending in TASKS.md; integration
   alone is not proof that a build is validated.
3. Verify that both the previous `develop` and the intended feature commits
   remain ancestors, review the resulting feature set and run the checks
   appropriate to the changes. Publish to `origin/develop` when requested
   or included in the human's integration request.
4. Keep the feature branch independent. An upstream PR comes from that
   branch, never from `develop`: it must not include other personal features
   or these fork-specific documents.

Do not wait for an upstream maintainer to accept a feature before making an
authorized personal integration. Conversely, do not merge an upstream PR,
publish a release or describe a build as official just because the feature
is available in `develop`. Follow the official PR and release rules for
those separate actions.

## Bringing in official updates

1. Fetch `upstream` and `origin`; compare their current commits rather than
   relying on an earlier session's status.
2. Update clean local `main` to `upstream/main` by fast-forward. Synchronize
   `origin/main` when authorized. If `main` has diverged, inspect and explain
   the divergence before changing its history.
3. Merge the official baseline into `develop`, preserving personal features
   and current upstream behavior. Resolve each conflict from both branches
   and check semantic interactions even when Git merges code automatically.
4. Review and validate the result before publishing the updated `develop`.
   Feature branches with upstream PRs are updated separately when needed;
   updating `develop` does not update those PRs.

Never discard edits, remove untracked files or delete a stash to make a pull
work. Preserve unfinished work on its feature worktree or in an identified,
verified backup. Do not restore personal changes onto the mirror `main` by
default. A worktree with another agent's pending edits is not an integration
workspace.

## Where to record information

- This file holds the fork's working rules. Keep the startup link in
  AGENTS.md when integrating official changes, so agents can discover it.
- WISHLIST.md holds desired features and investigation ideas only. Read it
  for context; do not treat the whole wishlist as an authorized task list.
- [fork-docs/](fork-docs/README.md) holds personal-fork research epics,
  decisions and task folders. Read the relevant epic before starting one of
  its tasks. Research records and acceptance checklists are not evidence of
  implementation or human validation.
- [Collaboration guidance](fork-docs/COLLABORATION.md) scopes research,
  implementation, review and authorized integration. Project skills in
  `.agents/skills/` and the reviewer in `.codex/agents/` reference these rules.
  [The tracker](fork-docs/TRACKER.md) generates HTML from canonical Markdown;
  it is not a second backlog. No MCP is configured by this toolkit.
- TASKS.md records active implementation, integrated features, validation
  status, upstream issue/PR links and remaining work. Update only the lines
  belonging to the current task.
- Feature-specific user instructions belong in the existing relevant guides.

Keep this file, `fork-docs/`, personal project skills/reviewer/tools and the
fork additions to AGENTS.md on `develop`
and personal branches derived from it. Do not copy them into the mirror
`main`, submit them upstream or alter the official wiki as part of this
personal workflow.
Do not change the fork's default branch or CI/release configuration unless
the human asks for that separately.
