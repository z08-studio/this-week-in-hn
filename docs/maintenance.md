# Maintenance

This repository holds the publication assets and reviewed issue archive for **This Week in HN**. Its companion, [gen-newsletter-hn](https://github.com/z08-studio/gen-newsletter-hn), owns collection, ranking, generation, and the sole content template at `templates/formatted_template.md`. Both repositories remain private and closed source.

## Editorial workflow

1. Collect Hacker News posts submitted within an explicit seven-day window in the generator workspace.
2. Review the candidates, original sources, discussion links, and engagement snapshots.
3. Run `./scripts/newsletter.sh new` to create an empty draft, copy the generator's reviewed Formatted output into it, and edit the issue.
4. Publish manually on Fridays at [This Week in HN on Substack](https://thisweekinhn.substack.com/).
5. Run `./scripts/newsletter.sh archive YYYY-MM-DD-issue-NN.md` after publication is confirmed to save the published edition in `archive/YYYY/`.

The generator configures the section structure. Drafts and their attachments are ignored by Git. Read the [editorial contract](editorial-contract.md) for source and publication rules.

Hacker News is the public discovery source. This project has no public suggestion form or external contribution workflow. Issues and Wiki are disabled.

## Drafts and archives

Requirements: Bash and the system `date` command on macOS or Linux. No API key or elevated privileges are required.

Create an empty draft for the upcoming Friday in `Asia/Shanghai`:

```sh
./scripts/newsletter.sh new
```

On Friday, the default is today. On other days, it is the next Friday. An explicit date overrides the default and may use any valid calendar date:

```sh
./scripts/newsletter.sh new 2026-10-30
```

With no existing issues, this creates the empty file `drafts/2026-10-30-issue-01.md`. Issue numbering continues from the highest number in regular drafts and archives. Existing editions for the same date are preserved, and a future draft blocks creation of an earlier edition. The command does not generate or publish content.

After publishing and confirming the final content, archive the matching draft:

```sh
./scripts/newsletter.sh archive 2026-10-30-issue-01.md
```

Omit the filename only when there is exactly one regular draft with a valid issue filename and calendar date. Notes, directories, and symbolic links are not archive candidates. Only files directly inside `drafts/` can be archived, and existing archive files are never replaced. Drafts remain ignored by Git until archived.

## Repository layout

- `assets/avatar.png`: the approved H1 orange folded H logo, preserved from its original master.
- `assets/banner.png`: the orange README masthead, matching the Obsidian banner's editorial style.
- `drafts/`: ignored, unpublished working material.
- `archive/`: reviewed editions after publication.
- `docs/`: maintenance and editorial guidance.
- `scripts/newsletter.sh`: executable draft creation and archive helper.
- `tests/`: isolated draft and archive checks.

## Checks

```sh
bash -n scripts/newsletter.sh
python3 -B -m unittest discover -s tests -v
```

Tests use temporary fixtures and do not modify real issues.

## Rights and access

Original project material is proprietary; see [LICENSE](../LICENSE). Linked third-party material retains its original ownership. Keep source links and write original editorial summaries.
