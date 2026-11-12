# parliament: Lok Sabha questions and answers

A family of the s1d-labs scrape pool.

| Project | Stored |
|---|---|
| `parliament-ls` | one record per question: house, session, number, date, subject, ministry, members, PDF links |
| `parliament-rs` | one record per Rajya Sabha question, with question and answer text, from session 190 onward |
| `parliament-docs` | the English answer PDF in the bucket and one record |

- sansad.in and rsdoc.nic.in answer GitHub runners (tested 2026-11-12), so the projects run there without a proxy (`geo=""`, `proxy=""`).
- Pace: 4 workers, 1 request per second per worker.
- Gaps: the site's API gives questions from the 17th Lok Sabha (2019) onward.

Setup: change `family.py`, then Actions -> setup. Tests: `python -m pytest tests`.
