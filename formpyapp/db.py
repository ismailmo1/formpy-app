import json

from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

from .api import parse_template_form
from .models import Answer, Coordinate2D, Question, Template, User
from .views import app

mongo = PyMongo(app, "mongodb://127.0.0.1:27017/formpyapp")

db = mongo.db
import mongoengine as me

me.connect(host="mongodb://127.0.0.1:27017/formpyapp")


def create_template_coords(template_coords: str):
    all_coords = []
    for coords in json.loads(template_coords):
        x, y = coords
        coordinate = Coordinate2D(x_coordinate=x, y_coordinate=y)
        all_coords.append(coordinate)
    return all_coords


def create_template_questions(
    template_questions: dict,
    username: str = "user",
) -> Template:

    questions = []
    for qn in template_questions.items():
        answers = []
        qn_name = qn[0]
        qn_mult = True if qn[1]["multiple"] == "True" else False
        for ans in qn[1]["answers"].items():
            x, y = (int(coord) for coord in ans[1]["answer_coords"].split(","))
            coordinates = Coordinate2D(x_coordinate=x, y_coordinate=y)
            answer = Answer(
                coordinates=coordinates, value=ans[1]["answer_val"]
            )
            answers.append(answer)

        question = Question(
            question_value=qn_name,
            multiple_choice=qn_mult,
            answers=answers,
        )
        questions.append(question)

    return questions


def create_template(questions, template_name, user, all_coords):

    template = Template(
        name=template_name,
        questions=questions,
        owner=user,
        detected_spots=all_coords,
        category_tags=["testing"],
    )
    return template


def save_template(request_form):
    question_data = request_form
    template_name = request_form["templateName"]
    template_coords = f'[{request_form["coords"]}]'
    template_dict = parse_template_form(question_data)
    # db.template_dict_to_model(template_name, template_coords, template_dict)
    user = current_user()
    all_coords = create_template_coords(template_coords)
    all_questions = create_template_questions(template_dict)
    template = create_template(all_questions, template_name, user, all_coords)
    return template.save()


def update_template(template_id: str, template_dict: dict):
    template = get_template(template_id)


def get_all_templates() -> list:
    """return list of existing templates"""
    # template_cursor = db.templates.find()
    template_list = list(Template.objects)
    # template_list = [temp for temp in template_cursor]
    return template_list


def remove_template(template_id: str) -> bool:
    """delete template from db, return true on success"""
    template = Template.objects(id=template_id)
    return template.delete()


def get_template(template_id) -> dict:
    found_template = Template.objects(id=template_id).first()
    return found_template


def current_user():
    user = User(username="username", email="test@test.com")
    return user.save()
