# Maintenance

This repository holds the publication assets and reviewed issue archive for **This Week in HN**. Its companion, [gen-newsletter-hn](https://github.com/z08-studio/gen-newsletter-hn), owns collection, ranking, generation, and the sole content template at `templates/formatted_template.md`. Both repositories remain private and closed source.

## Editorial workflow

1. Collect Hacker News posts submitted within an explicit seven-day window in the generator workspace.
2. Review the candidates, original sources, discussion links, and engagement snapshots.
3. Create an empty Markdown file in `drafts/` named `YYYY-MM-DD-issue-NN.md`, copy the generator's reviewed Formatted output into it, and edit the issue.
4. Publish manually on Fridays at [This Week in HN on Substack](https://thisweekinhn.substack.com/).
5. Save the published edition in `archive/YYYY/YYYY-MM-DD-issue-NN.md` after publication is confirmed.

The generator configures the section structure. Drafts and their attachments are ignored by Git. Read the [editorial contract](editorial-contract.md) for source and publication rules.

Hacker News is the public discovery source. This project has no public suggestion form or external contribution workflow. Issues and Wiki are disabled.

## Repository layout

- `assets/avatar.png`: the approved H1 orange folded H logo, preserved from its original master.
- `assets/banner.png`: the orange README masthead, matching the Obsidian banner's editorial style.
- `drafts/`: ignored, unpublished working material.
- `archive/`: reviewed editions after publication.
- `docs/`: maintenance and editorial guidance.

## Rights and access

Original project material is proprietary; see [LICENSE](../LICENSE). Linked third-party material retains its original ownership. Keep source links and write original editorial summaries.
