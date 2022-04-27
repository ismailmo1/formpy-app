import pytest
from app.formpyapp import create_app


@pytest.fixture()
def app():
    app = create_app("config/test_config.py")
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture(app)
def client():
    return app.test_client()


@pytest.fixture()
def create_question(create_answer):
    from app.formpyapp.db.models import Question

    question = Question(
        answers=create_answer,
        question_value="question test",
        multiple_choice=False,
    )

    return question
