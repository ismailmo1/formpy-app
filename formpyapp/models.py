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


class User(Document):
    username = StringField(max_length=15, min_length=2, required=True)
    first_name = StringField(max_length=15)
    last_name = StringField(max_length=15)
    email = EmailField(required=True)


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
    name = StringField(required=True)
    public = BooleanField(default=True)
    questions = EmbeddedDocumentListField(Question, required=True)
    owner = ReferenceField(User, required=True)
    # hold all detected spots (including ones not assigned)
    detected_spots = EmbeddedDocumentListField(Coordinate2D, required=False)
    # i.e. what category the template belongs to: school quiz, manufacturing, public survey etc
    category_tags = ListField(StringField(max_length=10))

    def to_dict():
        """return dictionary than can be read by formpy template.fromdict method
        question_config in form
        {question_id:{multiple:bool, answers:list[answer]}, question_id2}
        """
        pass