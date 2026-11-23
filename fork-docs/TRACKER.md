# Canonical research and the offline tracker

[Index](README.md) · [Collaboration](COLLABORATION.md)

## Commands

From any fork checkout containing this toolkit:

```sh
python3 scripts/fork-tracker.py status
python3 scripts/fork-tracker.py validate
python3 scripts/fork-tracker.py build
```

The build writes `.scratch/fork-tracker/index.html`, which is ignored. Open it
in a browser without a server. For a personal presentation elsewhere, pass
`build --output /path/to/presentation.html`. Repository outputs are restricted
to `.scratch/`; exporting does not change Markdown or Git state. Python 3.11+
and its standard library are sufficient; no package installation, MCP, model,
remote service or build toolchain is required.

All fork Markdown is embedded for offline navigation. Links to code, official
documentation and external evidence require Internet. Source links refer to
the personal fork's `develop` branch; an unintegrated local edit may differ
from that online source. The fingerprint identifies the exact local Markdown
snapshot used for this presentation. The generated timestamp does not verify
sources or advance any task.

## Task metadata

Each `fork-docs/epics/<epic>/tasks/<ID>/README.md` starts with metadata between
`---` lines. Use one `key: "JSON-quoted string"` per line. This restricted
YAML-compatible format is deliberate: the generator needs no YAML dependency.
The task body remains ordinary Markdown. The skill includes a reusable template.

Required keys: `id`, `title`, `area`, `stage`, `interest`, `researched`,
`updated`, `summary`, `next_step`, `evidence`.

- `id` is globally unique and matches the task folder, for example GFX-001.
- `researched` is the original review date, not the last build; `updated` is
  the meaningful record-update date. Both use ISO dates; leave `researched`
  empty only for an idea that has not been researched yet.
- `interest` records personal interest, not the team project board's Priority.
- `summary` and `next_step` feed the presentation directly.
- `evidence` is empty through analysis. From prototype onward, it must name
  an existing, nonempty repository Markdown record, relative to the task file.
  Keep the evidence within the relevant task folder when possible.

| Stage | Evidence expected |
| --- | --- |
| `idea` | Outcome identified; fact finding pending |
| `analysed` | Sources, feasibility limits and a proposed next step recorded |
| `prototype` | Bounded executable experiment and its limitations recorded |
| `measured` | Reproducible local observations and method recorded |
| `validated` | Explicit human acceptance, date and accepted conditions recorded |
| `integrated` | Authorized integration commit and remaining checks recorded |

These are milestones, not percentages. Counts in the presentation are
cumulative: a measured task also has a prototype. Validation checks syntax,
references and the presence of an evidence record; it cannot certify that
the record is true. Review its contents before advancing a stage and update
the corresponding TASKS.md entry when active implementation changes.

## Supported document syntax

Headings, paragraphs, simple lists/checklists, tables, fenced code, inline code,
bold text and Markdown links. Raw HTML is escaped. The generated view is
read-only; pending checklist items are shown as pending text. Navigation among
embedded Markdown documents stays offline. Unsupported link schemes or local
paths outside the repository are rejected. Keep source links and examples
simple rather than depending on a full Markdown engine.

## Historical personal tracker

The earlier Spanish files are an archive of the initial discussion. Their
presentation entrypoint can delegate to this versioned generator against a
develop checkout. It must not read those archived task files to reconstruct
current status. If that checkout moves, select another toolkit checkout; no
new copy of the canonical analysis is needed.
