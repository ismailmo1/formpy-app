import json

import mongoengine as me
from flask_login import current_user
from mongoengine.queryset.visitor import Q

from .api import parse_template_form
from .models import Answer, Coordinate2D, Question, Template, User
from .views import app

me.connect(host="mongodb://127.0.0.1:27017/formpyapp")


def create_template_coords(template_coords: str):
    all_coords = []
    for coords in json.loads(template_coords):
        x, y = coords
        coordinate = Coordinate2D(x_coordinate=x, y_coordinate=y)
        all_coords.append(coordinate)
    return all_coords


def create_template_questions(template_questions: dict) -> Template:

    questions = []
    for qn in template_questions.items():
        answers = []
        qn_name = qn[0]
        qn_mult = True if qn[1]["multiple"] == "True" else False
        for ans in qn[1]["answers"]:
            x, y = (int(coord) for coord in ans["answer_coords"].split(","))
            coordinates = Coordinate2D(x_coordinate=x, y_coordinate=y)
            answer = Answer(coordinates=coordinates, value=ans["answer_val"])
            answers.append(answer)

        question = Question(
            question_value=qn_name,
            multiple_choice=qn_mult,
            answers=answers,
        )
        questions.append(question)

    return questions


def create_template(questions, template_name, user, public):

    template = Template(
        name=template_name,
        questions=questions,
        owner=user,
        category_tags=["testing"],
        public=public,
    )
    return template


def save_template(request_form, owner: User = None):
    template_name = request_form["templateName"]
    # public = False if no public key defined in form
    public = bool(request_form.get("public"))
    request_form.pop("templateName")
    request_form.pop("public")
    question_data = request_form

    all_questions = create_template_questions(question_data)

    template = create_template(all_questions, template_name, owner, public)
    return template.save()


def update_template(template_id: str, request_form):
    curr_template = get_template(template_id)
    curr_template.name = request_form["templateName"]
    curr_template.public = bool(request_form.get("public"))

    template_dict = parse_template_form(request_form)
    all_questions = create_template_questions(template_dict)
    curr_template.questions = all_questions

    # not updating/editing coords yet (future with fabricjs frontend)
    # template_coords = f'[{request_form["coords"]}]'
    # all_coords = create_template_coords(template_coords)
    # curr_template.detected_spots = all_coords

    # add "public" and category tags update when added to form
    return curr_template.save()


def get_public_templates() -> list:
    """return list of public templates"""
    template_list = list(Template.objects(public=True))
    return template_list


def get_user_templates(user: User) -> list:
    """return list of private user templates"""
    template_list = list(Template.objects(Q(owner=user) & Q(public=False)))
    return template_list


def remove_template(template_id: str) -> bool:
    """delete template from db by owner only, return true on success"""
    template = Template.objects(id=template_id)
    if template.owner == current_user:
        return template.delete()


def make_templates_public(owner):
    templates = get_user_templates(owner)
    for template in templates:
        template.public = True
        template.save()


def remove_user_templates(owner, private_only=True) -> int:
    """delete user templates

    Args:
        owner ([type]): user object whose templates to delete
        private_only (bool, optional): Delete only user's private templates. Defaults to True.

    Returns:
        int: number of deleted documents
    """
    if private_only:
        templates = Template.objects(Q(owner=owner) & Q(public=False))
    else:
        templates = Template.objects(owner=owner)

    return templates.delete()


def get_template(template_id) -> dict:
    found_template = Template.objects(id=template_id).first()
    return found_template
