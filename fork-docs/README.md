# Personal fork documentation

Research, epics and implementation plans specific to the personal fork.
Follow [FORK_WORKFLOW.md](../FORK_WORKFLOW.md) and
[AGENTS.md](../AGENTS.md) before working on an entry.

These documents belong on personal `develop` and branches derived from it.
Keep them out of the official `main` mirror, upstream feature PRs and the
official wiki. The separate `fork-docs/` tree intentionally avoids adding
personal research to the upstream `docs/` wiki catalogue.

## Epics

| Epic | Research status | Implementation status | Next task |
| --- | --- | --- | --- |
| [Apple Silicon graphics](epics/apple-silicon-graphics/README.md) | Initial analysis recorded | No prototype or local measurements | [GFX-001: native MetalFX temporal reconstruction](epics/apple-silicon-graphics/tasks/GFX-001/README.md) |

## Keeping the records useful

- [WISHLIST.md](../WISHLIST.md) records desired features and links to research.
- An epic records the common analysis, dependencies, decisions and task index.
- Each task has its own folder, stable ID, acceptance criteria and evidence
  status. Keep future implementation notes and measurement records there.
- [TASKS.md](../TASKS.md) records active implementation, personal integration
  and outstanding validation; update only the current task's entries.
- Source review, hardware support, a working prototype, a measurement and
  human acceptance are separate facts. A documentation merge proves none
  of the runtime milestones.
- Mark the original source-review date separately from later document edits.
  Recheck API versions, project licences and upstream activity before coding.

Use English in this repository. The personal Spanish presentation is a
separate local artifact; it is not the authoritative implementation record.
Do not commit proprietary model weights, runtime DLLs, cache contents,
personal paths, grid data or credentials as research evidence.
