import json
from unittest.mock import patch

import cv2
from werkzeug.datastructures import FileStorage


def test_upload_template_img(client):
    with open("tests/artifacts/images/simple_qna.jpeg", "rb") as f:
        image_file = {"uploadedTemplate": FileStorage(f)}
        res = client.post("/upload-template", data=image_file)

    assert res.status_code == 200
    assert res.json["pts"] == [
        [110.0, 76.0],
        [2322.0, 75.0],
        [2322.0, 1575.0],
        [110.0, 1575.0],
    ]

    assert len(res.json["img"]) == 479372


def test_upload_template_pdf(client):
    with open("tests/artifacts/pdf/simple_qna.pdf", "rb") as f:
        image_data = {"uploadedTemplate": FileStorage(f)}
        res = client.post("/upload-template", data=image_data)

    assert res.status_code == 200
    assert res.json["pts"] == [
        [69.0, 67.0],
        [2283.0, 66.0],
        [2283.0, 1568.0],
        [72.0, 1569.0],
    ]
    assert len(res.json["img"]) == 148428


def test_align_template(client):
    from app.api.img_proc import img_to_str

    test_img_str = img_to_str(
        cv2.imread("tests/artifacts/images/simple_qna_aligned.png")
    )

    with open("tests/artifacts/images/simple_qna_misalign.jpeg", "rb") as f:
        misaligned_img_data = {
            "uploadedTemplate": FileStorage(f),
            "custom": "false",
            "pts": "[[129.0, 191.0], [1987.0, 48.0], [2083.0, 1309.0], [225.0, 1452.0]]",
        }

        res = client.post("/align-template", data=misaligned_img_data)

    aligned_img_str = res.json["img"]

    assert aligned_img_str == test_img_str


def test_define_template(logged_in_client, db_user):
    from app.db.utils import delete_image, remove_template

    with open("tests/artifacts/json/template_data.json") as f:
        template_data = json.load(f)

    with open("tests/artifacts/img_to_str.txt") as f:
        img_str_data = f.read()

    template_data[
        "uploadedTemplate"
    ] = f"data:image/jpeg;base64, {img_str_data}"
    headers = {"Content-Type": "application/json"}

    res = logged_in_client.post(
        "/define-template/new", data=json.dumps(template_data), headers=headers
    )

    assert res.status_code == 200
    assert res.content_type == "application/json"
    res_dict = json.loads(res.json)

    assert res_dict["name"] == "test template"
    assert len(res_dict["questions"][0]["answers"]) == 3

    # cleanup images and db
    template_id = res_dict["_id"]["$oid"]
    img_name = res_dict["img_name"]
    assert delete_image(img_name)
    with patch("app.db.utils.current_user", db_user):
        assert remove_template(template_id)


def test_read_forms_get(client, db_template):
    res = client.get("/read")

    assert res.status_code == 200
    assert b"test template" in res.data
    assert b"Upload your completed forms" in res.data
    assert b"Read Forms" in res.data


def test_read_forms_post(client, db_simple_template):

    with open("tests/artifacts/images/simple_qna_straight.jpeg", "rb") as f:
        form_data = {
            "formImg": [FileStorage(f)],
            "templateId": db_simple_template.id,
        }

        res = client.post("/read", data=form_data)

    assert res.status_code == 200
    assert res.json["answers"] == [
        {
            "1": ["b"],
            "2": ["a"],
            "3": ["b"],
            "4": ["d"],
            "5": ["c"],
            "6": ["a"],
        }
    ]
