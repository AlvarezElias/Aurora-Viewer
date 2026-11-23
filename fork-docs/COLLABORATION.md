# Working together on the personal fork

Follow [AGENTS.md](../AGENTS.md) and [FORK_WORKFLOW.md](../FORK_WORKFLOW.md).
This page records only the personal collaboration choices that supplement
those rules. It does not override host permissions or create standing
authorization for unrelated tasks.

## Match the requested action

- **Discuss / investigate:** inspect and explain; preserve changing claims as
  dated evidence when documenting. Do not start renderer implementation.
- **Document:** update the relevant epic, tasks and decisions; regenerate the
  presentation from them. A documentation request alone is not a Git push.
- **Implement:** work on the selected task and its validation in an isolated
  task branch/worktree. The wishlist is context, not a queue to execute.
- **Integrate into develop:** complete the named personal integration through
  the fork workflow. Preserve existing authorization through the task; do not
  ask again solely because a step is commit, merge or push. Different
  destinations, destructive recovery and actual permission gates still matter.
- **Review:** inspect the explicit target and base, return findings, and keep
  edits and integration outside scope unless separately requested.

Continue useful authorized work and make routine reversible choices. Ask only
when missing information materially changes the result or an actual approval
is required. Explain the specific reason when blocked; never reinterpret a
refusal as authorization or bypass a host/branch protection.

## Communication and records

Use the human's language in conversation and English in repository/GitHub
artifacts. Give concise progress updates about findings, decisions and the
next uncertainty. At handoff state the outcome, actual checks, evidence limits
and what requires the human. Distinguish research, a prototype, local
measurements, human acceptance and personal integration.

Canonical research lives in `fork-docs/`. The HTML is a generated view. Change
the Markdown first and regenerate it; do not advance a status in the HTML or
maintain a separately translated backlog. Keep source-review dates distinct
from document-update and presentation-build dates. See [TRACKER.md](TRACKER.md).

## Available workflows

| Need | Project capability |
| --- | --- |
| Branch/worktree selection or authorized personal integration | `$aurora-fork-flow` |
| Turn a discussion into research/tasks or update the presentation | `$aurora-research-to-epic` |
| Plan or record an actual graphics experiment | `$aurora-gfx-validation` |
| Independent review when requested | `aurora-reviewer`, defined in `.codex/agents/aurora-reviewer.toml` |

Skills live in `.agents/skills/`. The reviewer inherits session permissions;
its no-edit instructions do not create a separate sandbox. Use delegation
only when requested or otherwise explicitly authorized by applicable
instructions; defining the profile does not launch it. No MCP is configured
by this toolkit; that integration remains deferred.

The helper `python3 scripts/fork-tracker.py status` inventories local state
without fetching, changing refs or launching a compiler. Missing tools are
reported rather than treated as successful checks. It does not replace fresh
Git refs or required AGENTS.md verification.

These instructions, project skills, reviewer definition and presentation tools
stay on personal branches/develop, outside the official mirror and upstream PRs.
