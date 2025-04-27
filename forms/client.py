from flask_wtf import FlaskForm  
from wtforms import StringField, SelectField, SubmitField  
from wtforms.validators import DataRequired, Length, Regexp

def coerce_int_or_none(value):  
   if value is None or value == 'None' or value == '':  
    return None  
    return int(value)

class ClientForm(FlaskForm):  
    uid = StringField('UID', validators=[  
        DataRequired(),  
        Length(min=1, max=4),  
        Regexp(r'^[0-9]+$', message='UID може містити тільки цифри')  
    ])  
    full_name = StringField('ПІБ', validators=[  
        DataRequired(),  
        Length(min=5, max=100)  
    ])  
    street_id = SelectField('Вулиця', coerce=int, validators=[DataRequired()])  
    house_number = StringField('Номер будинку', validators=[  
        DataRequired(),  
        Length(max=10)  
    ])  
    apartment = StringField('Квартира', validators=[Length(max=10)])  
    tariff_id = SelectField('Тариф', coerce=int, validators=[DataRequired()])  
    
    # Оновлення equipment_id для обробки None  
    equipment_id = SelectField('Обладнання', choices=[(None, "Відсутнє")], coerce=coerce_int_or_none)  
    
    submit = SubmitField('Зберегти')
    
class FilterForm(FlaskForm):  
    search = StringField('Пошук')  
    street = SelectField('Вулиця', choices=[])  
    tariff = SelectField('Тариф', choices=[])
    