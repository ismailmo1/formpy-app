import json


def test_create_template(client):
    res = client.get("/create")

    assert res.status_code == 200
    assert b"Create" in res.data
    assert b"Upload your template file (pdf or image)" in res.data
    assert (
        b'<form method="POST" enctype="multipart/form-data" id="uploadImgForm">'
        in res.data
    )


def test_delete_template(db_template, logged_in_client):
    template_id = db_template.id
    res = logged_in_client.get(f"/delete/{template_id}", follow_redirects=True)

    assert res.status_code == 200
    assert res.request.path == "/view"
    assert b"template deleted!" in res.data


def test_edit_template(client, db_template):
    res = client.get(f"/edit/{db_template.id}")

    assert res.status_code == 200

    # template rendered with script tag to load template json into canvas
    # assertion to check if template loaded correctly
    assert (
        b'name\\": \\"test template\\", \\"public\\": true, \\'
        b'"questions\\": [{\\"question_value\\": \\"question test\\", '
        b'\\"multiple_choice\\": false, \\"answers\\": [{\\"coordinates\\": '
        b'{\\"x_coordinate\\": 200, \\"y_coordinate\\": 500}, \\"value\\": '
        b'\\"test answer\\"}]}], '
    ) in res.data


def test_update_template(client, db_template):
    template_id = db_template.id

    with open("tests/artifacts/json/update_template_data.json", "r") as f:
        update_data = json.dumps(json.load(f))

    headers = {"Content-Type": "application/json"}

    res = client.post(
        f"update-template/{template_id}", data=update_data, headers=headers
    )

    assert res.status_code == 200
    assert "updated test template" in res.json
    assert "updated_ans1" in res.json
    assert (
        '{"coordinates": {"x_coordinate": 300, "y_coordinate": 400}, "value": "updated_ans2"}'
        in res.json
    )
