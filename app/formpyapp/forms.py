from flask_wtf import FlaskForm
from wtforms.fields.core import (
    FieldList,
    FormField,
    IntegerField,
    RadioField,
    StringField,
)
from wtforms.fields.simple import (
    BooleanField,
    FileField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
)

from .models import User


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


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")
    remember_me = BooleanField("Remember Me")


# taken from grinberg's helloworld
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=15)]
    )
    first_name = StringField("First Name", validators=[Length(max=15)])
    last_name = StringField("Last Name", validators=[Length(max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    # custom validators automatically called by form.validate()
    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class EditUserForm(RegistrationForm):
    submit = SubmitField("Submit")


class DeleteUserForm(FlaskForm):
    delete_options = RadioField(
        label="Template Deletion Options",
        choices=[
            ("none", "Keep my templates and make them public"),
            ("private", "Delete all my private templates"),
            ("all", "Delete all my templates"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Delete Account")
