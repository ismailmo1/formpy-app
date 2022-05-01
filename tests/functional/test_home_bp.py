def test_home(client):
    res = client.get("/home")

    assert res.status_code == 200
    assert b"src=/static/videos/promo.webm" in res.data
    assert b"Get Started" in res.data
    assert b"http://www.ismailmo.com" in res.data


def test_start(client):
    res = client.get("/getting-started")

    assert res.status_code == 200
    assert b"Quick Start Guide" in res.data
    assert b"Step 1 - Create your form document" in res.data
    assert b"Step 2 - Define your form template" in res.data
    assert b"Step 3 - Print and Collect Data" in res.data
    assert b"Step 4 - Read your forms" in res.data


def test_starter_doc(client):
    res = client.get("/starter-doc")

    assert res.status_code == 200
    assert res.content_type == "application/vnd.oasis.opendocument.text"
    assert "formpy-starter-doc.odt" in res.headers["Content-Disposition"]


def test_view_template(client, db_template):
    res = client.get("/view")

    assert res.status_code == 200
    assert str(db_template.id) in str(res.data)
    assert db_template.name in str(res.data)
    assert db_template.img_name in str(res.data)
