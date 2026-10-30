import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class NewsletterScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("scripts", "drafts", "archive"):
            (self.root / directory).mkdir()
        shutil.copy2(REPO_ROOT / "scripts/newsletter.sh", self.root / "scripts/newsletter.sh")

    def run_script(self, *args, env=None):
        return subprocess.run(
            [str(self.root / "scripts/newsletter.sh"), *args],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
        )

    def test_first_issue_creates_an_empty_draft(self):
        result = self.run_script("new", "2026-10-30")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "drafts/2026-10-30-issue-01.md").read_bytes(), b"")

    def test_default_date_uses_upcoming_friday_in_shanghai_including_today(self):
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        fake_date = bin_dir / "date"
        fake_date.write_text(
            '#!/bin/bash\n'
            'if [[ "$1" == "+%u" ]]; then\n'
            '    [[ "$TZ" == "Asia/Shanghai" ]] || exit 1\n'
            '    printf "%s\\n" "$NEWSLETTER_TEST_WEEKDAY"\n'
            'elif [[ "$1" == "-d" && "$2" == "+$NEWSLETTER_TEST_DAYS days" ]]; then\n'
            '    [[ "$NEWSLETTER_TEST_DATE_STYLE" == "gnu" ]] || exit 1\n'
            '    [[ "$TZ" == "Asia/Shanghai" ]] || exit 1\n'
            '    printf "%s\\n" "$NEWSLETTER_TEST_FRIDAY"\n'
            'elif [[ "$1" == "-v+${NEWSLETTER_TEST_DAYS}d" ]]; then\n'
            '    [[ "$TZ" == "Asia/Shanghai" ]] || exit 1\n'
            '    printf "%s\\n" "$NEWSLETTER_TEST_FRIDAY"\n'
            'else\n'
            '    exec "$NEWSLETTER_TEST_DATE" "$@"\n'
            'fi\n'
        )
        fake_date.chmod(0o755)
        env = dict(os.environ)
        env["NEWSLETTER_TEST_DATE"] = shutil.which("date")
        env["PATH"] = str(bin_dir) + os.pathsep + env["PATH"]
        env["TZ"] = "Pacific/Honolulu"

        for date_style in ("gnu", "bsd"):
            for weekday, days, friday in (
                (4, 1, "2026-10-30"),
                (5, 0, "2026-10-30"),
                (6, 6, "2026-11-06"),
                (7, 5, "2026-11-06"),
            ):
                with self.subTest(date_style=date_style, weekday=weekday):
                    env["NEWSLETTER_TEST_DATE_STYLE"] = date_style
                    env["NEWSLETTER_TEST_WEEKDAY"] = str(weekday)
                    env["NEWSLETTER_TEST_DAYS"] = str(days)
                    env["NEWSLETTER_TEST_FRIDAY"] = friday
                    result = self.run_script("new", env=env)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    draft = self.root / "drafts" / f"{friday}-issue-01.md"
                    self.assertEqual(draft.read_bytes(), b"")
                    draft.unlink()

    def test_explicit_date_overrides_friday_schedule(self):
        result = self.run_script("new", "2026-10-29")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "drafts/2026-10-29-issue-01.md").exists())

    def test_numbering_uses_drafts_and_archives_in_base_ten(self):
        (self.root / "archive/2026").mkdir()
        (self.root / "archive/2026/2026-10-16-issue-08.md").write_text("Published\n")
        (self.root / "drafts/2026-10-23-issue-09.md").write_text("Draft\n")
        result = self.run_script("new", "2026-10-30")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "drafts/2026-10-30-issue-10.md").read_bytes(), b"")

    def test_unrelated_and_invalid_entries_do_not_affect_numbering(self):
        (self.root / "drafts/notes.md").write_text("Notes\n")
        (self.root / "drafts/2026-02-30-issue-90.md").write_text("Invalid date\n")
        (self.root / "drafts/2030-01-04-issue-99.md").mkdir()
        external = self.root / "external.md"
        external.write_text("Outside drafts\n")
        (self.root / "drafts/2030-01-11-issue-98.md").symlink_to(external)
        result = self.run_script("new", "2026-10-30")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "drafts/2026-10-30-issue-01.md").exists())

    def test_invalid_dates_leave_drafts_empty(self):
        for publication_date in ("2026-02-30", "2026-1-6", "tomorrow"):
            with self.subTest(publication_date=publication_date):
                result = self.run_script("new", publication_date)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(list((self.root / "drafts").iterdir()), [])

    def test_existing_draft_or_archive_prevents_duplicate_date(self):
        (self.root / "archive/2026").mkdir()
        for directory in ("drafts", "archive/2026"):
            with self.subTest(directory=directory):
                existing = self.root / directory / "2026-10-30-issue-01.md"
                existing.write_text("Existing issue\n")
                result = self.run_script("new", "2026-10-30")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("already exists", result.stderr)
                self.assertEqual(existing.read_text(), "Existing issue\n")
                self.assertFalse((self.root / "drafts/2026-10-30-issue-02.md").exists())
                existing.unlink()

    def test_future_draft_blocks_earlier_publication_date(self):
        existing = self.root / "drafts/2026-11-06-issue-01.md"
        existing.write_text("Future draft\n")
        result = self.run_script("new", "2026-10-30")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("dated after 2026-10-30", result.stderr)
        self.assertEqual(existing.read_text(), "Future draft\n")
        self.assertEqual(list((self.root / "drafts").iterdir()), [existing])

    def test_create_and_archive_round_trip(self):
        created = self.run_script("new", "2026-10-30")
        self.assertEqual(created.returncode, 0, created.stderr)
        draft = self.root / "drafts/2026-10-30-issue-01.md"
        content = "# This Week in HN #1\n\n- [A reviewed item](https://example.com/)\n"
        draft.write_text(content)
        archived = self.run_script("archive", draft.name)
        self.assertEqual(archived.returncode, 0, archived.stderr)
        self.assertFalse(draft.exists())
        self.assertEqual(
            (self.root / "archive/2026/2026-10-30-issue-01.md").read_text(), content
        )

    def test_archive_selects_only_regular_valid_issue_files(self):
        draft = self.root / "drafts/2026-10-30-issue-01.md"
        draft.write_text("Reviewed issue\n")
        (self.root / "drafts/notes.md").write_text("Notes\n")
        (self.root / "drafts/2026-02-30-issue-02.md").write_text("Invalid date\n")
        (self.root / "drafts/2026-11-06-issue-03.md").mkdir()
        result = self.run_script("archive")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(draft.exists())
        self.assertEqual((self.root / "drafts/notes.md").read_text(), "Notes\n")

    def test_archive_requires_a_choice_when_multiple_drafts_exist(self):
        for filename in ("2026-10-30-issue-01.md", "2026-11-06-issue-02.md"):
            (self.root / "drafts" / filename).write_text("Draft\n")
        result = self.run_script("archive")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Multiple drafts", result.stderr)
        self.assertEqual(len(list((self.root / "drafts").iterdir())), 2)

    def test_archive_does_not_replace_existing_files_or_symlinks(self):
        (self.root / "archive/2026").mkdir()
        draft = self.root / "drafts/2026-10-30-issue-01.md"
        archive = self.root / "archive/2026/2026-10-30-issue-01.md"
        draft.write_text("Draft\n")
        archive.write_text("Published\n")
        result = self.run_script("archive", draft.name)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(draft.read_text(), "Draft\n")
        self.assertEqual(archive.read_text(), "Published\n")
        archive.unlink()
        archive.symlink_to(self.root / "missing.md")
        result = self.run_script("archive", draft.name)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(archive.is_symlink())
        self.assertEqual(draft.read_text(), "Draft\n")

    def test_archive_rejects_external_files_and_symlinks(self):
        external = self.root / "2026-10-30-issue-01.md"
        external.write_text("Outside drafts\n")
        result = self.run_script("archive", str(external))
        self.assertNotEqual(result.returncode, 0)
        symlink = self.root / "drafts" / external.name
        symlink.symlink_to(external)
        result = self.run_script("archive", symlink.name)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(symlink.is_symlink())
        self.assertEqual(external.read_text(), "Outside drafts\n")

    def test_archive_rejects_invalid_filenames_dates_and_directories(self):
        for filename in ("notes.md", "2026-02-30-issue-01.md", "2026-10-30-issue-x.md"):
            with self.subTest(filename=filename):
                draft = self.root / "drafts" / filename
                draft.write_text("Draft\n")
                result = self.run_script("archive", filename)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(draft.read_text(), "Draft\n")
                draft.unlink()
        directory = self.root / "drafts/2026-10-30-issue-01.md"
        directory.mkdir()
        result = self.run_script("archive", directory.name)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(directory.is_dir())


if __name__ == "__main__":
    unittest.main()
