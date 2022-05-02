from collections import defaultdict
from typing import Tuple

import cv2
import numpy as np
from app.api.img_proc import read_form_img
from app.db import models
from app.db.utils import get_image_path
from formpy.form import Form
from formpy.template import Template


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


def read_form(template_id: str, form_img: str) -> Tuple[np.ndarray, dict]:
    """read form and return image of detected qns and form obj

    Args:
        template_id (str): id of selected template to read form against
        form_img (str): bin64 str of form image
    """
    template = models.Template.objects(id=template_id).first()
    template_dict = template.to_dict()

    template_img_path = get_image_path(template_id)
    img = read_form_img(form_img)

    # scale image to match template image size
    # scaled_img = cv2.resize(
    #     img, template_img.shape, interpolation=cv2.INTER_LINEAR
    # )

    template = Template.from_dict(
        template=template_dict,
        img_path=template_img_path,
    )
    form = Form(img, template)
    qn_ans = {}
    for qn in form.questions:
        qn_ans[qn] = qn.find_answers(form.img)

    qn_ans_vals = {
        qn.question_id: [ans.value for ans in answers]
        for (qn, answers) in qn_ans.items()
    }

    # cv2.destroyAllWindows()
    return form.mark_all_answers(), qn_ans_vals
