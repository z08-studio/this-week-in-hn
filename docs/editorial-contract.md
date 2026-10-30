# Editorial contract

## Approved project scope

This Week in HN collects Hacker News posts from the preceding week and turns them into an edited weekly newsletter. The publication archive is public and MIT licensed; the generator remains private and closed source. This project has no public submission workflow.

## Candidate and issue boundaries

- Use an explicit start and end for each seven-day submission window. Record the timezone and treat the end as exclusive.
- Submission time determines membership in the week. Source article publication time is separate and may be older.
- Retain the original title, original source link when available, and Hacker News discussion link.
- Capture points, comment count, and the time those metrics were observed. Do not describe lifetime snapshot counts as activity earned during the week.
- Check removed or dead items before inclusion. Failed retrieval or incomplete coverage must remain visible to the editor.
- Write original summaries after reviewing the linked material. A title-only candidate does not establish that an article or its comments have been reviewed.
- Give each story one primary place in the issue. Keep related discussion links without repeating the same story across sections.

The generator's Formatted workflow owns the issue layout and configured sections. Copy reviewed Formatted output into each new blank draft; this repository does not maintain a content template. Remove empty sections and unresolved placeholders before publication.

## Manual publication

Keep drafts in the ignored `drafts/` directory. Copy only reviewed content from the generator. Creating a repository or generating a draft does not publish an issue.

The publication is released every Friday at [This Week in HN on Substack](https://thisweekinhn.substack.com/). Archive a final issue only after its publication has been confirmed.
