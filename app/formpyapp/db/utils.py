import os

import cv2
import numpy as np
from app.formpyapp.db.models import (
    Answer,
    Coordinate2D,
    Question,
    Template,
    User,
)
from flask import current_app
from flask_login import current_user
from mongoengine.queryset.visitor import Q


def save_template(request_form, owner: User = None):
    template_name = request_form["templateName"]
    # public = False if no public key defined in form
    public = bool(request_form.get("public"))

    question_data = request_form["questions"]

    questions = create_template_questions(question_data)

    template = Template(
        name=template_name,
        questions=questions,
        owner=owner,
        category_tags=["testing"],
        public=public,
    )
    return template.save()


def update_template(template_id: str, request_form):
    curr_template = get_template(template_id)
    template_name = request_form["templateName"]
    # public = False if no public key defined in form
    public = bool(request_form.get("public"))

    question_data = request_form["questions"]

    curr_template.name = template_name
    curr_template.public = public
    questions = create_template_questions(question_data)

    curr_template.questions = questions

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
    """delete template from db by owner only"""
    template = Template.objects(id=template_id).first()
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


def get_all_templates(current_user):
    templates = get_public_templates()
    if current_user.is_authenticated:
        user = User.objects(id=current_user.id).first()
        user_templates = get_user_templates(user)
        templates.extend(user_templates)

    return templates


def get_image(template_id: str, img_path: str | None = None) -> np.ndarray:
    """get image from template id

    Args:
        template_id (str): template id
    """
    if img_path == None:
        img_path = current_app.config["IMG_STORAGE_PATH"]
    template = Template.objects(id=template_id).first()
    img_path = os.path.join(img_path, f"{template.img_name}.jpeg")

    img = cv2.imread(img_path)

    return img


def delete_image(template_id: str, img_path: str | None = None) -> bool:
    """delete image from template id, return true if deleted

    Args:
        template_id (str): template id
    """
    if img_path == None:
        img_path = current_app.config["IMG_STORAGE_PATH"]
    img_path = os.path.join(img_path, f"{template_id}.jpeg")

    if os.path.isfile(img_path):
        os.remove(img_path)
        return True

    return False


def save_template_image(
    img: np.ndarray,
    img_id: str,
    img_path: str | None = None,
) -> str:
    """add 5% padding and save image in location storage

    Args:
        img (np.ndarray): image to save
        img_id (str): objectID of template

    Returns:
        str: path of saved image
    """
    if img_path == None:
        img_path = current_app.config["IMG_STORAGE_PATH"]

    save_img_path = os.path.join(img_path, f"{img_id}.jpeg")
    # add 5% padding
    horizontal_border = int(img.shape[0] * 0.05)
    vertical_border = int(img.shape[1] * 0.05)

    padded_img = cv2.copyMakeBorder(
        img,
        horizontal_border,
        horizontal_border,
        vertical_border,
        vertical_border,
        cv2.BORDER_CONSTANT,
        None,
        (255, 255, 255),
    )
    if cv2.imwrite(save_img_path, padded_img):
        return save_img_path
    else:
        return None


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
            question_value=qn_name, multiple_choice=qn_mult, answers=answers
        )
        questions.append(question)

    return questions
