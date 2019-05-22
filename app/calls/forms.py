from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    IntegerField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)

from app import db
from app.models import Role, User

class CreateCallForm(Form):
    call_name = StringField(
        'Name the call', 
        validators=[InputRequired(), Length(1, 64)], 
        description="e.g. Sales Call 21May2019")
    num_callers = IntegerField(
        'How many people in total are going to be on your call?', 
        validators=[InputRequired()], 
        description="e.g. 3")
    initial_phone_number = StringField(
        "State the number that will be instantiating the phone call",
        validators=[InputRequired()],
        description="e.g. 2622717436"
    )
    phone_numbers = StringField(
        "List the numbers that will be on the call, EXCEPT your own, separated by ';'",
        validators=[InputRequired()], 
        description="e.g. 5433422178;9087544654"
    )

    submit = SubmitField('Start New Call')

    def validate(self):
        if not Form.validate(self):
            return False
        result = True
        
        n_callers = len(self.phone_numbers.data.split(';'))
        if n_callers != self.num_callers.data:
            result = False
        return result
