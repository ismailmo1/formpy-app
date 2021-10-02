from re import template

from flask_pymongo import PyMongo

from .views import app

mongo = PyMongo(app, "mongodb://127.0.0.1:27017/formpyapp")

db = mongo.db


def save_template(template_name: str, template_dict: dict) -> str:
    """save template json into template collection and return obj id"""
    template_dict["name"] = template_name
    result = db.templates.insert_one(template_dict)

    return result.inserted_id


def get_all_templates() -> list:
    """return list of existing templates"""
    template_cursor = db.templates.find()
    template_list = [temp for temp in template_cursor]
    return template_list
