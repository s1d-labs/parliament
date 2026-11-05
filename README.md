# parliament: Lok Sabha questions and answers

A family of the s1d-labs scrape pool.

| Project | Stored |
|---|---|
| `parliament-ls` | one record per question: house, session, number, date, subject, ministry, members, PDF links |
| `parliament-rs` | one record per Rajya Sabha question, with question and answer text, from session 190 onward |
| `parliament-docs` | the English answer PDF in the bucket and one record |

- sansad.in answers from India, so the projects use `geo="IN"`: India pool servers only.
- Pace: 4 workers, 1 request per second per worker.
- The PDFs (`parliament-docs`) wait until the question pages finish, because they would otherwise take the workers on this host.
- Gaps: the site's API gives questions from the 17th Lok Sabha (2019) onward.

Setup: change `family.py`, then Actions -> setup. Tests: `python -m pytest tests`.
