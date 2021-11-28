import base64
import io
import json
import os
from collections import defaultdict
from typing import Tuple

import cv2
import formpy.utils.img_processing as ip
import numpy as np
from formpy.questions import Form, Template
from formpy.utils.template_definition import find_spots
from PIL import Image

from . import models

IMG_STORAGE_PATH = "image_storage/template_images"


def img_to_str(img: np.array) -> str:
    """writes numpy array img to str

    Args:
        img (np.array): numpy array representation of image

    Returns:
        str: base64 string of image
    """
    img = Image.fromarray(img)
    img_buf = io.BytesIO()
    img.save(img_buf, "PNG")
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read())
    return str(img_base64).split("'")[1]


def str_to_img(img_str: str) -> np.array:
    """converts b64 img to np.array"""
    img_data = base64.b64decode(img_str)
    img_arr = np.fromstring(img_data, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    return img


def read_form_img(img_str: str) -> np.array:
    """reads image from web form"""
    img_arr = np.fromstring(img_str, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    return img


def align_img(img: np.array, json_pts: str) -> np.array:
    """aligns image with bounding box if detected

    Args:
        img (np.array): user uploaded image

    Returns:
        np.array: aligned image
    """
    pts = np.array(json.loads(json_pts), dtype="float32")
    ordered_pts = np.zeros((4, 2), dtype="float32")
    ordered_pts[0] = pts[np.argmin(pts.sum(axis=1))]
    ordered_pts[2] = pts[np.argmax(pts.sum(axis=1))]

    # smallest difference x-y = top right
    ordered_pts[1] = pts[np.argmin(np.diff(pts, axis=1))]
    # largest difference x-y = bottom left
    ordered_pts[3] = pts[np.argmax(np.diff(pts, axis=1))]
    aligned_img = ip.align_page(img, corner_pts=ordered_pts)

    return aligned_img


def get_bounding_pts(img: np.ndarray) -> tuple:
    pts = ip.get_outer_box(img)
    return pts


def parse_template_form(form: dict) -> dict:
    """return dict of template with web form from edit template/create template pages
    initialise empty questions dict to populate with question:answers[]
    question_config in form {question_id:{multiple:bool, answers: {answerid : {answer_coords:tuple, answer_val:str}}, question_id2}"""
    questions = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for data in form.items():
        name, att = data
        if name in [
            "templateName",
            "coords",
            "csrf_token",
            "public",
            "currTempId",
        ]:
            continue
        question_num, answer_details = name.split("-", maxsplit=1)
        ans_index, ans_type = answer_details.split("-")
        if ans_type == "index":
            questions[question_num]["answers"][ans_index][
                "answer_coords"
            ] = att
        elif ans_type == "value":
            questions[question_num]["answers"][ans_index]["answer_val"] = att
        elif ans_type == "multipleFlag":
            questions[question_num]["multiple"] = att

    return questions


def save_image(img: np.ndarray, img_id: str, img_path=IMG_STORAGE_PATH) -> str:
    """save image in location storage

    Args:
        img (np.ndarray): image to save
        img_id (str): objectID of template

    Returns:
        str: path of saved image
    """
    save_img_path = os.path.join(
        f"formpyapp/static/{img_path}", f"{img_id}.jpeg"
    )
    cv2.imwrite(save_img_path, img)
    return save_img_path


def get_image(
    template_id: str, img_path: str = IMG_STORAGE_PATH
) -> np.ndarray:
    """get image from template id

    Args:
        template_id (str): template id
    """
    template = models.Template.objects(id=template_id).first()
    img_path = os.path.join(
        f"formpyapp/static/{img_path}", f"{template.img_name}.jpeg"
    )

    img = cv2.imread(img_path)

    return img


def delete_image(template_id: str, img_path: str = IMG_STORAGE_PATH) -> bool:
    """delete image from template id, return true if deleted

    Args:
        template_id (str): template id
    """
    img_path = save_img_path = os.path.join(
        f"formpyapp/static/{img_path}", f"{template_id}.jpeg"
    )

    if os.path.isfile(img_path):
        os.remove(img_path)
        return True

    return False


def read_form(template_id: str, form_img: str) -> Tuple[np.ndarray, dict]:
    """read form and return image of detected qns and form obj

    Args:
        template_id (str): id of selected template to read form against
        form_img (str): bin64 str of form image
    """
    img = read_form_img(form_img)
    template_dict = (
        models.Template.objects(id=template_id).first().question_dict
    )
    template = Template.from_dict(img, template_dict)
    form = Form(img, template)
    qn_ans = {}
    for qn in form.questions:
        qn_ans[qn] = qn.find_answers(form.img)

    qn_ans_vals = {
        qn.question_id: [ans.value for ans in answers]
        for (qn, answers) in qn_ans.items()
    }
    return form.mark_all_answers(qn_ans, color=(255, 0, 0)), qn_ans_vals
