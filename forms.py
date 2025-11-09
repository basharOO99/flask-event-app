from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Optional
from datetime import datetime

class EventForm(FlaskForm):
    name = StringField(
        'Event Name', 
        validators=[DataRequired(message="Event name is required.")]
    )
    description = TextAreaField(
        'Event Description', 
        validators=[DataRequired(message="Description is required.")]
    )
    location = StringField(
        'Location', 
        validators=[Optional()]  # يمكن ترك الموقع فارغ
    )
    date = DateTimeField(
        'Event Date',
        default=datetime.utcnow,
        format='%Y-%m-%d %H:%M:%S',
        validators=[Optional()]  # إذا لم يُدخل المستخدم التاريخ سيتم استخدام UTC now
    )
    submit = SubmitField('Submit')
