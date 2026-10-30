# This Week in HN

Private editorial home for **This Week in HN**, a weekly digest of popular Hacker News stories, maintained by **z08 Studio** as part of Weekly Newsletter.

This repository holds a blank draft starter, brand proposals, and reviewed issue archive. Its private companion, [gen-newsletter-hn](https://github.com/z08-studio/gen-newsletter-hn), is the collection and generation workspace and owns the Formatted content template. Both repositories are private and closed source.

## Editorial workflow

1. Collect Hacker News posts submitted within an explicit seven-day window in the generator workspace.
2. Review the candidates, original sources, discussion links, and engagement snapshots.
3. Create an empty Markdown file in `drafts/`, copy the generator's reviewed Formatted output into it, and edit the issue.
4. Publish manually on the chosen newsletter platform.
5. Save the published edition in `archive/YYYY/YYYY-MM-DD-issue-NN.md`.

Hacker News is a public discovery source. This project does not need a public GitHub submission form or an external contribution workflow. Issues and Wiki are disabled.

## Repository layout

- `assets/logo/`: logo proposals and download assets; no proposal is approved until selected by the editor.
- `templates/newsletter-template.md`: empty starter for new files. The sole content template lives in the generator's `templates/formatted_template.md`.
- `drafts/`: ignored, unpublished working material.
- `archive/`: reviewed editions after publication; no editions have been published or imported here.
- `docs/editorial-contract.md`: scope and publication rules.

The publication weekday, Substack address, and final logo selection are not set. Section structure is configured in the companion generator. Do not infer a Tuesday or Monday schedule from the other newsletters.

## Rights and access

Original project material is proprietary; see [LICENSE](LICENSE). Linked third-party material retains its original ownership. Keep source links and write original editorial summaries.
