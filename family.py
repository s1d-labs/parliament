"""What this family scrapes: Lok Sabha questions and answers from sansad.in, every question of the 17th and 18th Lok Sabha, and Rajya Sabha questions from rsdoc.nic.in.

parliament-ls   -- one queue item per page of 100 questions. Page 1 of a session adds the pages after it and the answer files.
parliament-docs -- one queue item per answer PDF (English).
"""
import json
from pathlib import Path

FAMILY = json.loads((Path(__file__).parent / "scrape.json").read_text())["family"]
HOST = "sansad.in"
# Lok Sabha number -> sessions the site lists. A session with no questions gives an empty page, which is harmless.
RS_HOST = "rsdoc.nic.in"
RS_SESSIONS = range(190, 276)
SESSIONS = {17: range(1, 16), 18: range(1, 12)}

PROJECTS = [
    {"name": f"{FAMILY}-ls", "title": "Lok Sabha questions", "task": "questions", "unit_label": "page", "record_label": "question",
     "items": [{"key": f"ls{ls}-s{s}-p1", "payload": {"ls": ls, "session": s, "page": 1}} for ls, ss in SESSIONS.items() for s in ss]},
    {"name": f"{FAMILY}-rs", "title": "Rajya Sabha questions and answers", "task": "rajya", "host": RS_HOST, "unit_label": "session", "record_label": "question",
     "items": [{"key": f"rs-s{n}", "payload": {"session": n}} for n in RS_SESSIONS]},
    {"name": f"{FAMILY}-docs", "title": "Lok Sabha answer PDFs", "task": "docs", "hold": True, "unit_label": "file", "record_label": "answer PDF", "items": []},
]
PROBES = [{"name": f"{FAMILY}:{RS_HOST}", "url": f"https://{RS_HOST}/question/GetAllministary", "expect": "MIN"}, {"name": f"{FAMILY}:{HOST}", "url": f"https://{HOST}/api_ls/question/qetFilteredQuestionsAns?loksabhaNo=18&sessionNumber=2&pageNo=1&locale=en&pageSize=1", "expect": "listOfQuestions"}]
