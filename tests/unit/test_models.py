import json


def test_new_user():
    # need to load inside func to allow fixture env vars to be set first
    from app.formpyapp.db.models import User

    user = User(
        username="ismailmo",
        first_name="ismail",
        last_name="mohammed",
        email="me@ismail.com",
    )
    user.set_password("password123")

    assert user.username == "ismailmo"
    assert user.first_name == "ismail"
    assert user.last_name == "mohammed"
    assert user.password_hash != "password123"
    assert user.email == "me@ismail.com"


def test_new_coordinate():
    from app.formpyapp.db.models import Coordinate2D

    coordinate = Coordinate2D(x_coordinate=100, y_coordinate=42)

    assert coordinate.x_coordinate == 100
    assert coordinate.y_coordinate == 42


def test_new_answer():
    from app.formpyapp.db.models import Answer, Coordinate2D

    coordinates = Coordinate2D(x_coordinate=200, y_coordinate=300)
    answer = Answer(coordinates=coordinates, value="test answer")

    assert answer.value == "test answer"
    assert answer.coordinates.x_coordinate == 200
    assert answer.coordinates.y_coordinate == 300


def test_new_question():
    from app.formpyapp.db.models import Answer, Coordinate2D, Question

    # create a bunch of answers
    answers = []
    for i in range(0, 3):
        coordinates = Coordinate2D(
            x_coordinate=i * 100, y_coordinate=(i * 100) + 100
        )
        answer = Answer(coordinates=coordinates, value=f"test answer {i}")
        answers.append(answer)

    question = Question(
        answers=answers,
        question_value="question test",
        multiple_choice=False,
    )

    assert question.question_value == "question test"
    assert question.multiple_choice == False
    assert question.answers[0].value == "test answer 0"
    assert question.answers[1].coordinates.x_coordinate == 100
    assert question.answers[2].coordinates.y_coordinate == 300


def test_new_template():
    from app.formpyapp.db.models import (
        Answer,
        Coordinate2D,
        Question,
        Template,
        User,
    )

    coordinates = Coordinate2D(x_coordinate=100, y_coordinate=200)
    answer = Answer(coordinates=coordinates, value=f"test answer")

    question = Question(
        answers=[answer],
        question_value="question test",
        multiple_choice=False,
    )
    user = User(username="ismailmo", email="ismail@ismail.com")

    template = Template(
        name="test template",
        public=True,
        questions=[question],
        owner=user,
        category_tags=["cat_1", "cat_2"],
    )

    assert template.name == "test template"
    assert template.owner == user
    assert template.category_tags == ["cat_1", "cat_2"]
    assert template.questions == [question]
    assert template.public == True
    assert json.dumps(template.to_dict()["questions"]) == (
        '{"question test": {"multiple": false, "answers": '
        '[{"answer_coords": [100, 200], "answer_val": "test answer"}]}}'
    )
