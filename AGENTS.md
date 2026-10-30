# Repository guidelines

- The publication is **This Week in HN**, part of **This Week In Newsletters**, maintained by z08 Studio.
- This publication and archive repository is public and MIT licensed. The companion `z08-studio/gen-newsletter-hn` remains private and closed source; keep collection, model configuration, credentials and unpublished material there.
- Use public Hacker News data for discovery. Do not add public submission forms, contribution invitations, issue templates, or community PR workflows.
- This repository owns brand assets and the reviewed archive. Create blank drafts and copy reviewed Formatted output into them. Maintain the content layout only in the companion generator; do not add a local `templates/` directory. Collection, ranking, and generation also belong in the generator.
- Keep tracked source, documentation, and newsletter content in English. Do not copy another project's secrets, runtime outputs, branding, or Git history.
- The approved identity is H1, the orange folded H. Use `assets/avatar.png` for the logo and `assets/banner.png` for the README masthead; obsolete logo proposals have been removed.
- The publication is released every Friday at `https://thisweekinhn.substack.com/`.
- Use `scripts/newsletter.sh new [YYYY-MM-DD]` to create an empty draft. The default is the upcoming Friday in Asia/Shanghai, including today on a Friday; an explicit valid calendar date overrides it. Number issues from `01` across regular drafts and archives. Never overwrite a draft or archive.
- Run `bash -n scripts/newsletter.sh` and `python3 -B -m unittest discover -s tests -v` after changing maintenance tools. Preserve the script's executable permission.
- Keep the README focused on readers: banner, short introduction, and subscription. Maintenance instructions live in `docs/maintenance.md`; do not add a public suggestion form.
- Keep unpublished drafts ignored. Publishing an issue and archiving it after publication require a direct user request. No command should publish automatically.
- This repository belongs to **This Week In Newsletters**. Commit directly to `main` by default; create a pull request only when the user explicitly requests one.
