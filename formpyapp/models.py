from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    BooleanField,
    EmailField,
    EmbeddedDocumentListField,
    IntField,
    ReferenceField,
    StringField,
)


class User(Document):
    username = StringField(max_length=15, min_length=2, required=True)
    first_name = StringField(max_length=15)
    last_name = StringField(max_length=15)
    email = EmailField(required=True)


class Answer(EmbeddedDocument):
    x_coordinate = IntField(required=True)
    y_coordinate = IntField(required=True)
    value = StringField(max_length=100, required=True)


class Question(EmbeddedDocument):
    question_value = StringField(max_length=200, required=True)
    multiple_choice = BooleanField(default=False)
    answers = EmbeddedDocumentListField(Answer, required=True)


class Template(Document):
    questions = EmbeddedDocumentListField(Question, required=True)
    owner = ReferenceField(User, required=True)
    # i.e. what category the template belongs to: school quiz, manufacturing, public survey etc
    category_tags = StringField(max_length=10)
