import json

from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

from .views import app

mongo = PyMongo(app, "mongodb://127.0.0.1:27017/formpyapp")

db = mongo.db


def save_template(
    template_name: str, template_coords: str, template_questions: dict
) -> str:
    """save template json into template collection and return obj id"""
    template_dict = {}
    template_dict["questions"] = template_questions
    template_dict["name"] = template_name
    template_dict["coords"] = json.loads(template_coords)

    result = db.templates.insert_one(template_dict)

    return result.inserted_id


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
