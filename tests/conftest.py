import time
from unittest.mock import patch

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

    yield test_app


@pytest.fixture()
def client(app):
    return app.test_client()


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
    )

    return template


@pytest.fixture(scope="function")
def db_user(app):
    from app.formpyapp.db.models import User

    user = User(
        username=f"test_user{str(time.time())[-6:]}",
        email=f"test{time.time()}@test.com",
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
