from collections import defaultdict
from uuid import uuid4

from flask_login import UserMixin
from formpyapp.views import login
from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    BooleanField,
    EmailField,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)
from mongoengine.queryset.base import NULLIFY
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, Document):
    username = StringField(
        max_length=15, min_length=2, required=True, unique=True
    )
    first_name = StringField(max_length=15)
    last_name = StringField(max_length=15)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Coordinate2D(EmbeddedDocument):
    x_coordinate = IntField(required=True)
    y_coordinate = IntField(required=True)


class Answer(EmbeddedDocument):
    coordinates = EmbeddedDocumentField(Coordinate2D)
    value = StringField(max_length=100, required=True)


class Question(EmbeddedDocument):
    question_value = StringField(max_length=200, required=True)
    multiple_choice = BooleanField(default=False)
    answers = EmbeddedDocumentListField(Answer, required=True)


class Template(Document):
    name = StringField(required=True, unique=True)
    public = BooleanField(default=True)
    questions = EmbeddedDocumentListField(Question, required=True)
    owner = ReferenceField(User, reverse_delete_rule=NULLIFY)
    # i.e. what category the template belongs to: school quiz, manufacturing, public survey etc
    category_tags = ListField(StringField(max_length=10))
    img_name = StringField(default=str(uuid4()))

    @property
    def question_dict(self):
        """return dictionary than can be read by formpy template.fromdict method
        question_config in form
        {question_id:{multiple:bool, answers:list[answer]}, question_id2}
        """
        question_dict = defaultdict(
            lambda: defaultdict(lambda: defaultdict(dict))
        )

        for question in self.questions:
            question_dict[question.question_value][
                "multiple"
            ] = question.multiple_choice
            for idx, ans in enumerate(question.answers):
                ans_dict = {
                    "answer_coords": f"{ans.coordinates.x_coordinate}, {ans.coordinates.y_coordinate}",
                    "answer_val": ans.value,
                }

                question_dict[question.question_value]["answers"][
                    f"answer{idx}"
                ] = ans_dict

        return question_dict


@login.user_loader
def load_user(id):
    return User.objects(id=id).first()
