# Repository guidelines

- The publication is **This Week in HN**, part of **This Week In Newsletters**, maintained by z08 Studio.
- This repository and `z08-studio/gen-newsletter-hn` must remain private and closed source. Do not add an open-source license or change repository visibility.
- Use public Hacker News data for discovery. Do not add public submission forms, contribution invitations, issue templates, or community PR workflows.
- This repository owns brand assets and the reviewed archive. Create blank drafts and copy reviewed Formatted output into them. Maintain the content template only in the companion generator's `templates/formatted_template.md`; do not add a local `templates/` directory. Collection, ranking, and generation also belong in the generator.
- Keep tracked source, documentation, and newsletter content in English. Do not copy another project's secrets, runtime outputs, branding, or Git history.
- The approved identity is H1, the orange folded H. Use `assets/avatar.png` for the logo and `assets/banner.png` for the README masthead; obsolete logo proposals have been removed.
- The publication is released every Friday at `https://thisweekinhn.substack.com/`.
- Keep the README focused on readers: banner, short introduction, and subscription. Maintenance instructions live in `docs/maintenance.md`; do not add a public suggestion form.
- Keep unpublished drafts ignored. Publishing an issue and archiving it after publication require a direct user request. No command should publish automatically.
- This repository belongs to **This Week In Newsletters**. Commit directly to `main` by default; create a pull request only when the user explicitly requests one.
