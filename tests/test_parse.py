from parse import date, doc_item, pages, rows, rs_rows, rs_url

ANSWER = [{"listOfQuestions": [{"quesNo": 280, "subjects": "Roads in Delhi", "lokNo": "18", "member": ["Shri A"], "ministry": "ROAD TRANSPORT AND HIGHWAYS", "type": "STARRED", "date": "09.08.2024", "questionsFilePath": "https://sansad.in/getFile/x.pdf?source=lsapps", "sessionNo": "2"}], "totalRecordSize": 3499}]


def test_rows():
    total, got = rows(ANSWER)
    assert total == 3499 and got[0][0] == "ls18-s2-S280-09.08.2024"
    assert got[0][1]["date"] == "2024-08-09" and got[0][1]["members"] == ["Shri A"]


def test_empty():
    assert rows([{"listOfQuestions": [], "totalRecordSize": 0}]) == (0, [])


def test_pages():
    assert pages(3499) == 35 and pages(100) == 1 and date("x") == ""


def test_doc_item():
    assert doc_item("a", {"pdf": "u", "lok_sabha": "18", "session": "2"})["payload"]["question"] == "a"


def test_rs():
    got = rs_rows([{"qno": 3290.0, "qslno": 7, "qtype": "UNSTARRED ", "ses_no": 268, "adate": "2025-08-21T00:00:00", "qtitle": "T", "min_name": "M", "name": "A"}])
    assert got[0][0] == "rs-s268-U3290-7" and got[0][1]["date"] == "2025-08-21" and got[0][1]["members"] == ["A"]
    assert rs_url(268).endswith("ses_no=268")
