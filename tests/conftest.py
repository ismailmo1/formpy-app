import json
from unittest.mock import patch

import cv2
import pytest


@pytest.fixture(scope="module")
def app():
    from app.formpyapp import create_app

    test_app = create_app("config/test_config.py")
    test_app.config.update(
        {
            "TESTING": True,
        }
    )

    with test_app.app_context():
        yield test_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def logged_in_client(client, db_user):

    with client:
        client.post(
            "/login",
            data={"username": "test_user", "password": "test"},
            follow_redirects=True,
        )
        yield client


@pytest.fixture()
def answer_model():
    from app.formpyapp.db.models import Answer, Coordinate2D

    coord = Coordinate2D(x_coordinate=200, y_coordinate=500)
    answer = Answer(coordinates=coord, value="test answer")

    return answer


@pytest.fixture()
def question_model(answer_model):
    from app.formpyapp.db.models import Question

    question = Question(
        answers=[answer_model],
        question_value="question test",
        multiple_choice=False,
    )

    return question


@pytest.fixture()
def template_model(question_model, db_user):
    from app.formpyapp.db.models import Template

    template = Template(
        name="test template",
        questions=[question_model],
        owner=db_user,
        category_tags=["testing"],
        public=True,
        img_name="simple_qna",
    )

    return template


@pytest.fixture(scope="function")
def db_user(app):
    from app.formpyapp.db.models import User

    user = User(
        username="test_user",
        email=f"test@test.com",
    )
    user.set_password("test")
    user.save()
    yield user
    user.delete()


@pytest.fixture()
def db_template(template_model, db_user):
    yield template_model.save()

    with patch("app.formpyapp.db.utils.current_user", db_user):
        template_model.delete()


@pytest.fixture()
def db_simple_template(db_user):
    from app.formpyapp.db.models import Template

    with open("/workspace/tests/artifacts/json/simple_qna.json") as f:
        template_data = json.load(f)

    template = Template(**template_data)
    template.owner = db_user
    yield template.save()

    with patch("app.formpyapp.db.utils.current_user", db_user):
        template.delete()


@pytest.fixture()
def simple_qna_img():
    return cv2.imread("tests/artifacts/images/simple_qna.jpeg")
