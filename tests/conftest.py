import os
from unittest import mock

import pytest


@pytest.fixture(scope="session", autouse=True)
def set_environment_vars():
    with mock.patch.dict(os.environ, {"IMG_STORAGE_PATH": "/"}):
        yield


@pytest.fixture()
def create_question(create_answer):
    from app.formpyapp.db.models import Question

    question = Question(
        answers=create_answer,
        question_value="question test",
        multiple_choice=False,
    )

    return question
