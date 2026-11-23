#!/usr/bin/env python3
"""Exercise tracker evidence gates, safe exports and read-only Git inspection."""

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("fork_tracker", Path(__file__).with_name("fork-tracker.py"))
tracker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tracker)


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.path = self.root / "fork-docs/epics/example/tasks/GFX-001/README.md"
        self.meta = dict(id="GFX-001", title="A real proposal", area="Graphics", stage="analysed",
                         interest="High", researched="2026-11-22", updated="2026-11-23",
                         summary="Research only", next_step="Measure a prototype", evidence="")
        self.write()
        template = self.root / "fork-docs/presentation/template.html"
        template.parent.mkdir(parents=True)
        template.write_text('<script id="tracker-data" type="application/json">__FORK_TRACKER_DATA__</script>')

    def write(self, body="# Proposal\n\n## Evidence\n\nNothing measured yet.\n", *, path=None, **changes):
        target = path or self.path
        target.parent.mkdir(parents=True, exist_ok=True)
        meta = {**self.meta, **changes}
        front = "---\n" + "\n".join(key + ": " + json.dumps(value) for key, value in meta.items()) + "\n---\n\n"
        target.write_text(front + body)

    def test_initial_research_is_not_a_prototype(self):
        records, _, _ = tracker.catalogue(self.root)
        self.assertEqual(records[0]["stage"], "analysed")
        self.assertEqual(records[0]["evidence"], "")

    def test_unresearched_idea_has_no_invented_review_date(self):
        self.write(stage="idea", researched="")
        records, _, _ = tracker.catalogue(self.root)
        self.assertEqual(records[0]["researched"], "")

    def test_researched_stage_needs_a_review_date(self):
        self.write(researched="")
        with self.assertRaisesRegex(ValueError, "source-review date"):
            tracker.catalogue(self.root)

    def test_unknown_stage_is_rejected(self):
        self.write(stage="probably-done")
        with self.assertRaisesRegex(ValueError, "unknown stage"):
            tracker.catalogue(self.root)

    def test_advanced_stage_requires_an_evidence_file(self):
        for stage in tracker.STAGES[2:]:
            with self.subTest(stage=stage):
                self.write(stage=stage)
                with self.assertRaisesRegex(ValueError, "evidence record"):
                    tracker.catalogue(self.root)

    def test_recorded_prototype_can_reference_its_evidence(self):
        (self.path.parent / "experiment.md").write_text("# Experiment\n\nObserved result and its limitations.\n")
        self.write(stage="prototype", evidence="experiment.md")
        records, _, _ = tracker.catalogue(self.root)
        self.assertEqual(records[0]["stage"], "prototype")

    def test_task_cannot_be_its_own_evidence(self):
        self.write(stage="measured", evidence="README.md")
        with self.assertRaisesRegex(ValueError, "evidence must"):
            tracker.catalogue(self.root)

    def test_evidence_cannot_escape_repository(self):
        self.write(stage="prototype", evidence="../../../../../../outside.md")
        with self.assertRaisesRegex(ValueError, "evidence must"):
            tracker.catalogue(self.root)

    def test_duplicate_ids_across_epics_fail(self):
        self.write(path=self.root / "fork-docs/epics/another/tasks/GFX-001/README.md")
        with self.assertRaisesRegex(ValueError, "Duplicate task ID"):
            tracker.catalogue(self.root)

    def test_update_cannot_predate_research(self):
        self.write(updated="2026-11-21")
        with self.assertRaisesRegex(ValueError, "predates"):
            tracker.catalogue(self.root)

    def test_links_and_anchors_are_validated(self):
        self.write("# Proposal\n\n[Evidence](#evidence)\n\n## Evidence\n\nPending.\n")
        self.assertEqual(tracker.catalogue(self.root)[2], 1)
        self.write("# Proposal\n\n[Missing](#unknown)\n")
        with self.assertRaisesRegex(ValueError, "unknown heading"):
            tracker.catalogue(self.root)

    def test_code_examples_are_not_followed_as_links(self):
        self.write("# Proposal\n\n```md\n[Example](missing.md)\n```\n")
        self.assertEqual(tracker.catalogue(self.root)[2], 0)

    def test_unsafe_link_schemes_are_rejected(self):
        self.write("# Proposal\n\n[Bad](javascript:alert(1))\n")
        with self.assertRaisesRegex(ValueError, "unsupported link scheme"):
            tracker.catalogue(self.root)

    def test_symlinked_sources_cannot_escape_repository(self):
        outside = self.root.parent / (self.root.name + "-outside.md")
        outside.write_text("# Outside\n")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        (self.root / "fork-docs/outside.md").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            tracker.catalogue(self.root)

    def test_payload_cannot_close_the_json_script(self):
        self.write('# Proposal\n\n<script>alert("x")</script>\n', summary="</script><script>bad()</script>")
        output = self.root / ".scratch/index.html"
        tracker.build(self.root, output)
        html = output.read_text()
        self.assertEqual(html.count("</script>"), 1)
        payload = json.loads(html.split('type="application/json">', 1)[1].rsplit("</script>", 1)[0])
        self.assertIn("&lt;script&gt;", payload["documents"]["fork-docs/epics/example/tasks/GFX-001/README.md"]["html"])

    def test_embedded_links_stay_offline(self):
        (self.path.parent / "notes.md").write_text("# Notes\n\nEvidence.\n")
        self.write("# Proposal\n\n[Notes](notes.md)\n")
        output = self.root / ".scratch/index.html"
        tracker.build(self.root, output)
        self.assertIn("#doc=fork-docs", output.read_text())

    def test_wrapped_list_items_keep_their_content_and_numbering(self):
        html = tracker.render_markdown("1. Check the device\n   before enabling it.\n2. Compare the results.\n\n- [ ] Record evidence\n  and limitations.\n", lambda href: href)
        self.assertIn("<ol><li>Check the device before enabling it.</li><li>Compare the results.</li></ol>", html)
        self.assertIn("<ul><li>Pending: Record evidence and limitations.</li></ul>", html)

    def test_failed_validation_preserves_existing_output(self):
        output = self.root / ".scratch/index.html"
        output.parent.mkdir()
        output.write_text("Previous presentation")
        self.write(stage="invalid")
        with self.assertRaises(ValueError):
            tracker.build(self.root, output)
        self.assertEqual(output.read_text(), "Previous presentation")

    def test_build_cannot_overwrite_canonical_files(self):
        template = self.root / "fork-docs/presentation/template.html"
        original = template.read_bytes()
        with self.assertRaisesRegex(ValueError, "ignored .scratch"):
            tracker.build(self.root, template)
        self.assertEqual(template.read_bytes(), original)
        with self.assertRaisesRegex(ValueError, "HTML file"):
            tracker.build(self.root, self.path)

    def test_fingerprint_changes_only_with_markdown_inputs(self):
        output = self.root / ".scratch/index.html"
        first = tracker.build(self.root, output)[2]
        self.assertEqual(first, tracker.build(self.root, output)[2])
        self.write("# Proposal\n\nA newly recorded finding.\n")
        self.assertNotEqual(first, tracker.build(self.root, output)[2])
        self.assertEqual(list(output.parent.glob("*.tmp")), [])

    def test_status_preserves_index_and_distinguishes_staged_changes(self):
        subprocess.run(["git", "init", "--initial-branch=develop", str(self.root)], check=True, capture_output=True)
        file = self.root / "fixture.txt"
        file.write_text("staged\n")
        subprocess.run(["git", "-C", str(self.root), "add", "fixture.txt"], check=True)
        file.write_text("edited after staging\n")
        index = self.root / ".git/index"
        before = index.read_bytes()
        result = tracker.status(self.root)
        self.assertIn("AM fixture.txt", result["changes"])
        self.assertEqual(index.read_bytes(), before)
        self.assertEqual(result["branch"], "develop")
        self.assertIsNone(result["refs"]["HEAD"])


if __name__ == "__main__":
    unittest.main()
