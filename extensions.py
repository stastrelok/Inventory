from flask_sqlalchemy import SQLAlchemy  
from flask_migrate import Migrate  
from flask_login import LoginManager  
from sqlalchemy import MetaData  
from flask_wtf.csrf import CSRFProtect

# Налаштування конвенції іменування  
convention = {  
    "ix": 'ix_%(column_0_label)s',  
    "uq": "uq_%(table_name)s_%(column_0_name)s",  
    "ck": "ck_%(table_name)s_%(constraint_name)s",  
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  
    "pk": "pk_%(table_name)s"  
}  

metadata = MetaData(naming_convention=convention)  
db = SQLAlchemy()  
migrate = Migrate()  
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  
login_manager.session_protection = "strong"
csrf = CSRFProtect()  

# Додаткові налаштування, якщо потрібно  
def configure_login_manager(app):  
    login_manager.init_app(app)  
    
    @login_manager.user_loader  
    def load_user(user_id):  
        from models.user import User  # Імпорт всередині функції для уникнення циклічного імпорту  
        return User.query.get(int(user_id))  