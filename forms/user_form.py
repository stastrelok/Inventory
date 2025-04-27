from flask_wtf import FlaskForm  
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField  
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError  
from models.user import User  

class UserForm(FlaskForm):  
    username = StringField('Ім\'я користувача', validators=[  
        DataRequired(message='Введіть ім\'я користувача'),  
        Length(min=3, max=50, message='Ім\'я має бути від 3 до 50 символів')  
    ])  
    
    email = StringField('Email', validators=[  
        DataRequired(message='Введіть email'),  
        Email(message='Некоректний формат email')  
    ])  
    
    password = PasswordField('Пароль', validators=[  
        Optional(),  
        Length(min=6, message='Пароль має бути не менше 6 символів')  
    ])  
    
    confirm_password = PasswordField('Підтвердження паролю', validators=[  
        Optional(),  
        EqualTo('password', message='Паролі не збігаються')  
    ])  
    
    role = SelectField('Роль', choices=[  
        ('admin', 'Адміністратор'),   
        ('manager', 'Менеджер'),   
        ('user', 'Користувач')  
    ], validators=[DataRequired(message='Оберіть роль')])  
    
    is_active = BooleanField('Активний обліковий запис')  
    submit = SubmitField('Зберегти')

    def validate_username(self, username):  
        user = User.query.filter_by(username=username.data).first()  
        if user:  
            raise ValidationError('Це ім\'я користувача вже зайняте')  

    def validate_email(self, email):  
        user = User.query.filter_by(email=email.data).first()  
        if user:  
            raise ValidationError('Ця електронна пошта вже використовується')