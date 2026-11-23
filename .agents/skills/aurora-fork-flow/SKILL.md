---
name: aurora-fork-flow
description: "Handle Aurora personal-fork branches, worktree selection and authorized integration into develop. Use for starting a fork task, committing or integrating it, or syncing the fork; not for ordinary research or documentation wording alone."
---

# Aurora fork flow

Resolve the repository root from the active checkout. Read its AGENTS.md and
FORK_WORKFLOW.md; the latter is the authority for branch destinations. Read
fork-docs/COLLABORATION.md for task scope and communication. Do not copy those
rules into another policy or assume that origin is the official repository.

## Select the operation

- Research or documentation requests do not imply implementation or a push.
- Start a personal task from current origin/develop; an upstream proposal
  needs an independent official-main base as the fork workflow explains.
- An integration request includes the named merge and publication to the
  fork when that is its stated scope. Reuse authorization already given for
  that task; a different destination or destructive recovery is a new action.
- Keep unrelated wishlist entries, official baseline updates, releases and
  upstream PR merges outside the current task unless separately requested.

## Execute with a checked destination

1. Run `python3 scripts/fork-tracker.py status` in the selected checkout.
   It reports branch, edits, local refs, worktrees and available tools without
   fetching or writing. Then verify actual remotes and refresh the required
   remote refs through ordinary Git. Cached refs are not current server state.
2. Reuse a suitable clean task-owned worktree or create one with the host's
   worktree tool. Never move another agent's pending edits to make room.
3. Create a focused `codex/` branch unless the human specifies another name.
   Develop only the requested change and update its TASKS.md entries.
4. Review the exact diff and run checks appropriate to the change plus the
   repository's required checks where available. Record unavailable tools and
   incomplete validation accurately; do not treat missing checks as passed.
5. Commit or push only within the request's scope. For personal integration,
   recheck a clean develop checkout, refresh origin, merge while preserving
   history, verify both prior develop and the intended task commit are
   ancestors, and review the resulting tree before a normal push.
6. A rejected push means refresh and inspect concurrent work; never force it.
   Report concrete conflicts or permission denials and preserve all work.

Documentation-only personal integration follows FORK_WORKFLOW.md; it does
not require creating an upstream PR. Viewer validation and any later upstream
PR retain their separate AGENTS.md gates. A sandbox escalation does not
expand scope; never work around a rejected approval or a protected branch.

## Handoff

Return the changed behaviour or artifact, branch and commit/merge reference,
actual checks, outstanding validation and next step. Use the human's language.
Clean up only task-owned worktrees through their host lifecycle tool; if it
refuses because a checkout is primary or in use, retain it and report that.
