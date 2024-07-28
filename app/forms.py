from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ExerciseForm(FlaskForm):
    exercise = StringField('Exercise', validators=[DataRequired()])
    count = IntegerField('Count', validators=[DataRequired()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add Exercise')
