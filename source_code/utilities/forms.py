"""
forms.py: Module to keep all the forms required by the application
Author: Shilpaj Bhalerao
Date: Aug 27, 2021
"""
# Standard Library Imports
import os
import urllib

# Third-Party Imports
import SharedArray as sa
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

# Local Imports
from source_code.utilities.custom_exceptions import ValidationError


# Attach it as a different array.
# shared_question_info = sa.attach("shm://test")
shared_question_info = "Phone Number"

# Login Form
class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Custom Validator for Phone Number Validation
class PhoneNumber(object):
    def __init__(self, message=None):
        if not message:
            message = f'Please Input a valid Phone Number'
        self.message = message

    def __call__(self, form, field):
        _data = field.data
        if _data.isdecimal():
            if len(_data) < 10 or len(_data) > 10 or _data[0] == "0":
                raise ValidationError(self.message)
        else:
            raise ValidationError(self.message)


class NumericValidator(object):
    def __init__(self, message=None):
        if not message:
            message = f'Please Input a valid Number'
        self.message = message

    def __call__(self, form, field):
        _data = field.data
        numeric_data = eval(_data)
        if not isinstance(numeric_data, (int, float)):
            raise ValidationError


class WebsiteLink(object):
    def __init__(self, message=None):
        if not message:
            message = f'Please Check the Website Link. Website non-responsive'
        self.message = message

    def __call__(self, form, field):
        url = field.data

        # Check if website is responsive
        status_code = urllib.request.urlopen(url).getcode()
        website_is_up = status_code == 200

        if not website_is_up:
            raise ValidationError(self.message)


class QuestionForm(FlaskForm):
    global shared_question_info

    # def __init__(self, question_type):
    #     super(QuestionForm, self).__init__()
    #     self.question_type = question_type

    # required_flag = True
    # submit = SubmitField('Okay')

    # quest = DataRequired() if self.required_flag else None
    phone_validator = PhoneNumber()
    website_validator = WebsiteLink()
    number_validator = NumericValidator()

    if shared_question_info == "Phone Number":
        # if quest:
        question = StringField("question", validators=[DataRequired()])
        question_description = StringField("question_description", validators=[DataRequired()])
        correct_answer = StringField("correct_answer", validators=[DataRequired(), phone_validator])
        submit = SubmitField("Okay")
    elif shared_question_info == "Website Link":
        question = StringField("question", validators=[DataRequired()])
        question_description = StringField("question_description", validators=[DataRequired()])
        correct_answer = StringField("correct_answer", validators=[DataRequired(), website_validator])
        submit = SubmitField("Okay")
    elif shared_question_info == "Number":
        question = StringField("question", validators=[DataRequired()])
        question_description = StringField("question_description", validators=[DataRequired()])
        correct_answer = StringField("correct_answer", validators=[DataRequired(), number_validator])
        submit = SubmitField("Okay")
    else:
        question = StringField("question", validators=[DataRequired()])
        question_description = StringField("question_description", validators=[DataRequired()])
        correct_answer = StringField("correct_answer", validators=[DataRequired(), phone_validator])
        submit = SubmitField("Okay")
