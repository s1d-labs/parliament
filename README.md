# parliament: Lok Sabha questions and answers

A family of the s1d-labs scrape pool.

| Project | Stored |
|---|---|
| `parliament-ls` | one record per question: house, session, number, date, subject, ministry, members, PDF links |
| `parliament-docs` | the English answer PDF in the bucket and one record |

- sansad.in answers from India, so the projects use `geo="IN"`: India pool servers only.
- Pace: 2 workers, 1 request per second per worker.
- Gaps: the site's API gives questions from the 17th Lok Sabha (2019) onward. Its Rajya Sabha API did not answer on 2026-11-04.

Setup: change `family.py`, then Actions -> setup. Tests: `python -m pytest tests`.
