#!/usr/bin/env python3
"""Validate fork research and build an offline presentation from canonical Markdown."""

import argparse
from datetime import date, datetime, timezone
import hashlib
from html import escape
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
STAGES = ("idea", "analysed", "prototype", "measured", "validated", "integrated")
FIELDS = {"id", "title", "area", "stage", "interest", "researched", "updated", "summary", "next_step", "evidence"}
LINK = re.compile(r"\[([^\]]+)\]\(([^\s]+)\)")


def read_record(path, root):
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Task source is outside the repository")
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not match:
        raise ValueError(f"{path.relative_to(root)}: missing task metadata")
    meta = {}
    for line in match[1].splitlines():
        key, sep, value = line.partition(":")
        key = key.strip()
        if not sep or key in meta or key not in FIELDS:
            raise ValueError(f"{path.name}: unknown or duplicate metadata key {key!r}")
        meta[key] = json.loads(value.strip())
    if meta.keys() != FIELDS or any(not isinstance(v, str) for v in meta.values()):
        raise ValueError(f"{path.name}: all metadata fields must be JSON-quoted strings")
    if any(not value.strip() for key, value in meta.items() if key not in ("evidence", "researched")):
        raise ValueError(f"{path.name}: empty metadata")
    if not re.fullmatch(r"[A-Z][A-Z0-9]*-\d{3,}", meta["id"]) or path.parent.name != meta["id"]:
        raise ValueError(f"{path.name}: task ID must match its folder")
    if meta["stage"] not in STAGES:
        raise ValueError(f"{path.name}: unknown stage {meta['stage']!r}")
    updated = date.fromisoformat(meta["updated"])
    researched = date.fromisoformat(meta["researched"]) if meta["researched"] else None
    if researched is None and meta["stage"] != "idea":
        raise ValueError(f"{path.name}: a researched stage requires its source-review date")
    if researched is not None and updated < researched:
        raise ValueError(f"{path.name}: update predates research")
    if STAGES.index(meta["stage"]) >= 2 and not meta["evidence"]:
        raise ValueError(f"{path.parent.name}: advancing beyond analysis requires an evidence record")
    if meta["evidence"]:
        evidence = (path.parent / meta["evidence"]).resolve()
        if evidence == path.resolve() or not evidence.is_relative_to(root.resolve()) or evidence.suffix != ".md" or not evidence.is_file():
            raise ValueError(f"{path.parent.name}: evidence must be an existing repository Markdown file")
        if not evidence.read_text(encoding="utf-8").strip():
            raise ValueError(f"{path.parent.name}: empty evidence record")
    return meta, match[2]


def body_text(text):
    """Exclude record metadata and fenced examples from link validation."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    return re.sub(r"(?ms)^```[^\n]*\n.*?^```\s*$", "", text)


def slug(text):
    return re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")


def local_link(path, href, root):
    parsed = urlsplit(href)
    if parsed.scheme:
        if parsed.scheme.lower() not in ("http", "https"):
            raise ValueError(f"{path.name}: unsupported link scheme")
        return None
    if href.startswith("//") or parsed.netloc or parsed.query:
        raise ValueError(f"{path.name}: unsupported local link")
    target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise ValueError(f"{path.relative_to(root)}: missing or out-of-repository link {href}")
    if parsed.fragment and target.suffix == ".md":
        headings = re.findall(r"^#{1,6}\s+(.+)$", body_text(target.read_text(encoding="utf-8")), re.M)
        if unquote(parsed.fragment) not in {slug(title) for title in headings}:
            raise ValueError(f"{path.name}: unknown heading in {href}")
    return target


def catalogue(root):
    root = root.resolve()
    documents = sorted((root / "fork-docs").rglob("*.md"))
    records, ids = [], set()
    for path in sorted((root / "fork-docs/epics").glob("*/tasks/*/README.md")):
        meta, body = read_record(path, root)
        if meta["id"] in ids:
            raise ValueError(f"Duplicate task ID: {meta['id']}")
        ids.add(meta["id"])
        records.append({**meta, "path": path.relative_to(root).as_posix(), "body": body})
    if not records:
        raise ValueError("No canonical task records found")
    links = 0
    for path in documents:
        if not path.resolve().is_relative_to(root):
            raise ValueError("Markdown source is outside the repository")
        text = body_text(path.read_text(encoding="utf-8"))
        for _, href in LINK.findall(text):
            if local_link(path, href, root) is not None:
                links += 1
    return records, documents, links


def inline(text, resolve):
    pattern = r"`([^`]+)`|\[([^\]]+)\]\(([^\s]+)\)|\*\*([^*]+)\*\*"
    out, end = [], 0
    for match in re.finditer(pattern, text):
        out.append(escape(text[end:match.start()]))
        code, label, href, bold = match.groups()
        if code is not None:
            out.append(f"<code>{escape(code)}</code>")
        elif label is not None:
            url = resolve(href)
            external = ' target="_blank" rel="noopener noreferrer"' if not url.startswith("#") else ""
            out.append(f'<a href="{escape(url, quote=True)}"{external}>{escape(label)}</a>')
        else:
            out.append(f"<strong>{escape(bold)}</strong>")
        end = match.end()
    out.append(escape(text[end:]))
    return "".join(out)


def render_markdown(text, resolve):
    """Render the documented subset, escaping raw HTML rather than executing it."""
    lines, out, i = text.strip().splitlines(), [], 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            out.append("<pre><code>" + escape("\n".join(code)) + "</code></pre>")
            i += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            if len(heading[1]) == 1:
                out.append(f'<span id="{escape(slug(heading[2]), quote=True)}"></span>')
                i += 1
                continue
            level = min(len(heading[1]) + 1, 6)
            out.append(f'<h{level} id="{escape(slug(heading[2]), quote=True)}">{inline(heading[2], resolve)}</h{level}>')
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"[\s|:\-]+", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                if not re.fullmatch(r"[\s|:\-]+", row):
                    rows.append([inline(cell.strip(), resolve) for cell in row.strip("|").split("|")])
                i += 1
            header = "".join(f'<th scope="col">{cell}</th>' for cell in rows[0])
            body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows[1:])
            out.append(f'<div class="table-scroll" tabindex="0" role="region" aria-label="Document table"><table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table></div>')
            continue
        item = re.match(r"^(- |\d+\. )(.+)$", line)
        if item:
            ordered = item[1] != "- "
            tag, items = ("ol" if ordered else "ul"), []
            while i < len(lines):
                item = re.match(r"^(- |\d+\. )(.+)$", lines[i].strip())
                if item is None or (item[1] != "- ") != ordered:
                    break
                content = item[2]
                i += 1
                while i < len(lines) and lines[i].strip() and lines[i].startswith(("  ", "\t")) and not re.match(r"^(- |\d+\. )", lines[i].strip()):
                    content += " " + lines[i].strip()
                    i += 1
                # Research checklists are evidence, not editable controls in this view.
                if content.startswith("[ ] "):
                    content = "Pending: " + content[4:]
                elif content.lower().startswith("[x] "):
                    content = "Recorded: " + content[4:]
                items.append("<li>" + inline(content, resolve) + "</li>")
            out.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||```|- |\d+\. )", lines[i].strip()):
            paragraph.append(lines[i].strip())
            i += 1
        out.append("<p>" + inline(" ".join(paragraph), resolve) + "</p>")
    return "\n".join(out)


def build(root, output):
    root = root.resolve()
    records, paths, links = catalogue(root)
    source_base = "https://github.com/AlvarezElias/Aurora-Viewer/blob/develop/"
    document_paths = {p.resolve() for p in paths}
    documents, fingerprint = {}, hashlib.sha256()
    for path in paths:
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        fingerprint.update(relative.encode() + b"\0" + text.encode() + b"\0")
        if re.match(r"\A---\n", text):
            _, text = read_record(path, root)

        def resolve(href, current=path):
            target = local_link(current, href, root)
            if target is None:
                return href
            parsed = urlsplit(href)
            target_relative = target.relative_to(root).as_posix()
            if target in document_paths:
                url = "#doc=" + quote(target_relative, safe="")
                if parsed.fragment:
                    url += "&section=" + quote(unquote(parsed.fragment), safe="")
                return url
            return source_base + quote(target_relative, safe="/") + ("#" + parsed.fragment if parsed.fragment else "")

        title = re.search(r"^#\s+(.+)$", text, re.M)
        documents[relative] = {
            "title": title[1] if title else path.stem,
            "html": render_markdown(text, resolve),
            "source": source_base + quote(relative, safe="/"),
        }
    payload = {
        "tasks": records, "documents": documents, "stages": STAGES,
        "fingerprint": fingerprint.hexdigest(),
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    template = (root / "fork-docs/presentation/template.html").read_text(encoding="utf-8")
    marker = "__FORK_TRACKER_DATA__"
    if template.count(marker) != 1:
        raise ValueError("Presentation must contain exactly one data marker")
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    rendered = template.replace(marker, data)
    output = output.resolve()
    if output.suffix.lower() not in (".html", ".htm"):
        raise ValueError("Presentation output must be an HTML file")
    if output.is_relative_to(root.resolve()) and ".scratch" not in output.relative_to(root.resolve()).parts:
        raise ValueError("Repository output must stay in ignored .scratch; use an external path for personal exports")
    # Validate everything before replacing an existing presentation.
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent, prefix=output.name + ".", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(rendered)
        temporary.replace(output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return len(records), links, fingerprint.hexdigest()


def git(root, *args, optional=False):
    process = subprocess.run(["git", "--no-optional-locks", "-C", str(root), *args], text=True, capture_output=True, check=False)
    if process.returncode and not optional:
        raise ValueError("Git inspection failed: " + " ".join(args))
    return process.stdout.rstrip("\n") if process.returncode == 0 else None


def status(root):
    """Read local state only; never fetch, stage, invoke compilers or modify refs."""
    branch = git(root, "symbolic-ref", "--short", "-q", "HEAD", optional=True)
    refs = {name: git(root, "rev-parse", "--verify", name, optional=True) for name in ("HEAD", "origin/develop", "upstream/main")}
    return {
        "branch": branch or "detached", "refs": refs,
        "changes": git(root, "status", "--porcelain=v1").splitlines(),
        "worktrees": git(root, "worktree", "list", "--porcelain").split("\n\n"),
        "platform": platform.system(),
        "tools": {tool: bool(shutil.which(tool)) for tool in ("git", "python3", "gh", "pwsh", "cargo", "rustfmt")},
        "remote_ref_freshness": "Local cache only; this inspection does not fetch or contact a server.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("status", "validate", "build"))
    parser.add_argument("--output", type=Path, help="Build output; defaults to ignored .scratch/fork-tracker/index.html")
    args = parser.parse_args()
    try:
        if args.command == "status":
            print(json.dumps(status(ROOT), indent=2))
        elif args.command == "validate":
            tasks, documents, links = catalogue(ROOT)
            print(f"Valid: {len(tasks)} tasks, {len(documents)} Markdown documents, {links} local links/anchors.")
        else:
            output = args.output or ROOT / ".scratch/fork-tracker/index.html"
            count, _, fingerprint = build(ROOT, output)
            print(f"Built {output}: {count} tasks; source fingerprint {fingerprint[:12]}.")
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
