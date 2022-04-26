from flask_wtf import FlaskForm
from wtforms.fields.core import FieldList, FormField, IntegerField, StringField
from wtforms.fields.simple import BooleanField, FileField
from wtforms.validators import DataRequired, Length


class CoordinateForm(FlaskForm):
    x = IntegerField()
    y = IntegerField()


class AnswerForm(CoordinateForm):
    value = StringField(validators=[Length(max=100)])


class QuestionForm(FlaskForm):
    question_value = StringField(validators=[Length(max=200), DataRequired()])
    multiple_choice = BooleanField(validators=[DataRequired()])
    answers = FieldList(FormField(AnswerForm), min_entries=1)


class DefineTemplateForm(FlaskForm):
    name = StringField()
    questions = FieldList(FormField(QuestionForm), min_entries=1)
    # hold all detected spots (including ones not assigned)
    detected_spots = FieldList(FormField(CoordinateForm))
    # i.e. what category the template belongs to: school quiz, manufacturing, public survey etc
    category_tags = FieldList(StringField(validators=[Length(max=100)]))
    public = BooleanField()
    img_name = FileField()
