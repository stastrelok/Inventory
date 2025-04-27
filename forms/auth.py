from flask_wtf import FlaskForm  
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email, Length, EqualTo  
 

class LoginForm(FlaskForm):  
    email = StringField('Email', validators=[DataRequired(), Email()])  
    password = PasswordField('Пароль', validators=[DataRequired()])  
    submit = SubmitField('Увійти')  

class RegistrationForm(FlaskForm):  
    username = StringField('Логін', validators=[  
        DataRequired(),  
        Length(min=4, max=20)  
    ])  
    email = StringField('Email', validators=[  
        DataRequired(),  
        Email()  
    ])  
    password = PasswordField('Пароль', validators=[  
        DataRequired(),  
        Length(min=6)  
    ])  
    password2 = PasswordField('Підтвердження пароля', validators=[  
        DataRequired(),  
        EqualTo('password', message='Паролі повинні співпадати')  
    ])  
    submit = SubmitField('Зареєструватися')