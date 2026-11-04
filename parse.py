"""Pure functions on the sansad.in answer."""
import datetime
import hashlib
import math

PAGE = 100


def url(ls, session, page):
    return f"https://sansad.in/api_ls/question/qetFilteredQuestionsAns?loksabhaNo={ls}&sessionNumber={session}&pageNo={page}&locale=en&pageSize={PAGE}"


def date(s):
    try:
        return datetime.datetime.strptime(s or "", "%d.%m.%Y").date().isoformat()
    except ValueError:
        return ""


def rows(answer):
    """-> (total questions in the session, [(record id, record)])"""
    d = answer[0] if isinstance(answer, list) and answer else {}
    out = []
    for q in d.get("listOfQuestions") or []:
        rid = f"ls{q.get('lokNo')}-s{q.get('sessionNo')}-{q.get('type', '')[:1]}{q.get('quesNo')}-{q.get('date')}"
        out.append((rid, {"house": "Lok Sabha", "lok_sabha": q.get("lokNo"), "session": q.get("sessionNo"), "number": q.get("quesNo"), "type": q.get("type"), "date": date(q.get("date")),
                          "subject": q.get("subjects"), "ministry": q.get("ministry"), "members": q.get("member") or [], "pdf": q.get("questionsFilePath") or "", "pdf_hindi": q.get("questionsFilePathHindi") or "", "doc": q.get("questionsDocPath") or "",
                          "question_text": q.get("questionText"), "answer_text": q.get("answerText"), "supplementary": q.get("supplementaryQuestionResDtoList") or []}))
    return d.get("totalRecordSize") or 0, out


def pages(total):
    return math.ceil(total / PAGE)


def doc_item(rid, rec):
    return {"key": hashlib.sha1(rec["pdf"].encode()).hexdigest()[:24], "payload": {"url": rec["pdf"], "question": rid, "ls": rec["lok_sabha"], "session": rec["session"]}}
