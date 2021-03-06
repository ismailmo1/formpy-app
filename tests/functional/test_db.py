import json
from unittest.mock import patch


def test_save_template(db_user):
    from app.db.models import Template
    from app.db.utils import remove_template, save_template

    with open("tests/artifacts/json/template_data.json") as f:
        template = json.load(f)

    template_id = save_template(template, db_user).id
    found_template = Template.objects(id=template_id).first()

    with patch("app.db.utils.current_user", db_user):
        remove_template(template_id)

    assert found_template.name == "test template"
    assert found_template.questions[0].multiple_choice == True


def test_update_template(db_user, db_template):
    # create template
    from app.db.models import Template
    from app.db.utils import update_template

    template_id = db_template.id

    with open("tests/artifacts/json/update_template_data.json") as f:
        update_data = json.load(f)

    updated_template_id = update_template(template_id, update_data).id

    updated_template = Template.objects(id=updated_template_id).first()

    assert updated_template.name == "updated test template"
    assert len(updated_template.questions) == 2
    assert updated_template.questions[1].answers[2].value == "updated_ans3"
    assert updated_template.public == True


def test_remove_template(db_user, db_template):
    from app.db.models import Template
    from app.db.utils import remove_template

    template_id = db_template.id
    remove_template(template_id)
    undeleted_template = Template.objects(id=template_id).first()

    assert undeleted_template is not None

    with patch("app.db.utils.current_user", db_user):
        remove_template(template_id)

    deleted_template = Template.objects(id=template_id).first()

    assert deleted_template is None


def test_get_template(db_user, db_template):
    from app.db.utils import get_template

    found_template = get_template(db_template.id)

    assert found_template.name == "test template"
    assert found_template.questions[0].multiple_choice == False
    assert found_template.questions[0].answers[0].value == "test answer"
    assert (
        found_template.questions[0].answers[0].coordinates.y_coordinate == 500
    )
