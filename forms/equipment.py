from flask_wtf import FlaskForm  
from wtforms import StringField, SelectField, SubmitField  
from wtforms.validators import DataRequired, Length, Optional  

class EquipmentForm(FlaskForm):  
    manufacturer = StringField('Виробник', validators=[DataRequired()])  
    model = StringField('Модель', validators=[DataRequired()])  
    serial_number = StringField('Серійний номер', validators=[DataRequired()])  
    mac_address = StringField('MAC адреса', validators=[Optional(), Length(min=17, max=17)])  
    status = SelectField('Статус', choices=[  
        ('available', 'Доступне'),  
        ('in_use', 'Використовується'),  
        ('written_off', 'Списане')  
    ])  
    submit = SubmitField('Зберегти')