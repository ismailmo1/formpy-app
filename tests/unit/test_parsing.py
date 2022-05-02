import json


def test_read_form(db_simple_template):
    import cv2
    from app.api.parsing import read_form

    form_img = cv2.imread("tests/artifacts/images/simple_qna_straight.jpeg")
    _, form_img_request = cv2.imencode(".jpg", form_img)
    marked_img, results = read_form(db_simple_template.id, form_img_request)

    assert results == {
        1: ["b"],
        2: ["a"],
        3: ["b"],
        4: ["d"],
        5: ["c"],
        6: ["a"],
    }

    assert list(marked_img[381, 1093]) == [0, 0, 255]
    assert list(marked_img[577, 793]) == [0, 0, 255]
    assert list(marked_img[771, 1092]) == [0, 0, 255]
    assert list(marked_img[967, 1679]) == [0, 0, 255]
    assert list(marked_img[1163, 1384]) == [0, 0, 255]
    assert list(marked_img[1361, 795]) == [0, 0, 255]


def test_create_template_question():
    from app.db.utils import create_template_questions

    with open("tests/artifacts/json/question_data.json", "r") as f:
        question_data = json.load(f)

    template_questions = create_template_questions(question_data)

    assert len(template_questions) == 1
    assert len(template_questions[0].answers) == 3
    assert template_questions[0].answers[0].value == "ans1"
    assert template_questions[0].answers[2].coordinates.x_coordinate == 661
    assert template_questions[0].answers[1].coordinates.y_coordinate == 460
