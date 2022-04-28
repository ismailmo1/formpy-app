import json


def test_save_template(user):
    import app.formpyapp.db.utils as utils
    from app.formpyapp.db.models import Template

    with open("tests/artifacts/json/template_data.json") as f:
        template = json.load(f)

    utils.save_template(template, user)
    saved_template = Template.objects().first()
    assert saved_template.name == "test template"
