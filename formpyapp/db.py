import json

from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

from .models import Answer, Coordinate2D, Question, Template, User
from .views import app

mongo = PyMongo(app, "mongodb://127.0.0.1:27017/formpyapp")

db = mongo.db
import mongoengine as me

me.connect(host="mongodb://127.0.0.1:27017/formpyapp")


# def save_template(
#     template_name: str, template_coords: str, template_questions: dict
# ) -> str:
#     """save template json into template collection and return obj id"""

#     template_dict = {}
#     template_dict["questions"] = template_questions
#     template_dict["name"] = template_name
#     template_dict["coords"] = json.loads(template_coords)

#     result = db.templates.insert_one(template_dict)

#     return result.inserted_id


def save_template(
    template_name: str,
    template_coords: str,
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
    user = User(username=username, email="test@test.com")
    user.save()
    all_coords = []

    for coords in json.loads(template_coords):
        x, y = coords
        coordinate = Coordinate2D(x_coordinate=x, y_coordinate=y)
        all_coords.append(coordinate)

    template = Template(
        name=template_name,
        questions=questions,
        owner=user,
        detected_spots=all_coords,
        category_tags=["testing"],
    )
    return template.save()


def update_template(template_id: str, template_dict: dict):
    """update template details from edit page form

    Args:
        template_id (str)
        template_dict (dict): dict from edit template form
    """
    update_result = db.templates.update_one(
        {"_id": ObjectId(template_id)}, {"$set": template_dict}
    )
    return update_result.raw_result


def get_all_templates() -> list:
    """return list of existing templates"""
    template_cursor = db.templates.find()
    template_list = [temp for temp in template_cursor]
    return template_list


def remove_template(template_id: str) -> bool:
    """delete template from db, return true on success"""
    try:
        id = ObjectId(template_id)
    except InvalidId as e:
        return False
    result = db.templates.delete_one({"_id": id})
    return result.deleted_count == 1


def get_template(template_id) -> dict:
    """return template dict"""
    try:
        id = ObjectId(template_id)
    except InvalidId as e:
        return None
    found_template = db.templates.find_one({"_id": id})
    return found_template
