from flask_wtf import FlaskForm  
from wtforms import StringField, SelectField, SubmitField  
from wtforms.validators import DataRequired  

class UserForm(FlaskForm):  
    username = StringField('Ім\'я користувача', validators=[DataRequired()])  
    role = SelectField('Роль', choices=[('адміністратор', 'Адміністратор'),   
                                          ('користувач', 'Користувач'),   
                                          ('гість', 'Гість')],   
                       validators=[DataRequired()])  
    submit = SubmitField('Додати користувача')