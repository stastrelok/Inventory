from flask_wtf import FlaskForm  
from wtforms import StringField, DecimalField, TextAreaField, SubmitField  
from wtforms.validators import DataRequired, Length, NumberRange  

class TariffForm(FlaskForm):  
    name = StringField('Назва тарифу', validators=[DataRequired(), Length(min=2, max=50)])  
    price = DecimalField('Ціна', validators=[DataRequired(), NumberRange(min=0)])  
    description = TextAreaField('Опис', validators=[Length(max=500)])  
    submit = SubmitField('Зберегти')