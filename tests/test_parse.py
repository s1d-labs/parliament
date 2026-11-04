from parse import date, doc_item, pages, rows

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
