from unittest.mock import patch

import pytest
from mongoengine import connect
from mongomock import MongoClient


class MongoMockClient(MongoClient):
    def init_app(self, app):
        return super().__init__()


@pytest.fixture()
def mongo():
    connect("test", "mongomock://localhost/")


@pytest.fixture()
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
def answer():
    pass


@pytest.fixture()
def question(answer):
    from app.formpyapp.db.models import Question

    question = Question(
        answers=answer,
        question_value="question test",
        multiple_choice=False,
    )

    return question


@pytest.fixture()
def template(question):
    from app.formpyapp.db.models import Template


@pytest.fixture()
def user(app):
    import app.formpyapp.db.utils as utils
    from app.formpyapp.db.models import User

    user = User(username="test_user", email="test@test.com")
    user.set_password("test")
    return user.save()
