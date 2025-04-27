from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField  
from wtforms.validators import DataRequired, Length  

class StreetForm(FlaskForm):  
    name = StringField('Назва вулиці', validators=[DataRequired(), Length(min=2, max=100)])  
    submit = SubmitField('Зберегти')