import os  
import secrets
from datetime import timedelta 
import logging 



class Config:  
    SECRET_KEY = 'testpassword'
    WTF_CSRF_SECRET_KEY = 'testpassword_csrf'   
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:stas19921010@localhost/inventory_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # Час життя сесії - 2 години 
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_SECURE = False  # Тільки HTTPS  
    SESSION_COOKIE_HTTPONLY = True  # Заборона доступу через JavaScript  
    SESSION_COOKIE_SAMESITE = 'Lax'  # Захист від CSRF  
    REMEMBER_COOKIE_DURATION = timedelta(days=14)  # Час життя "Запам'ятати мене"  
    REMEMBER_COOKIE_SECURE = False  # Тільки HTTPS  
    REMEMBER_COOKIE_HTTPONLY = True  # Заборона доступу через JavaScript  
    REMEMBER_COOKIE_SAMESITE = 'Lax'  
    WTF_CSRF_ENABLED = True  # Включити CSRF захист  
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_TIME_LIMIT = 3600  # Час життя CSRF токену (1 година)  
    SESSION_TYPE = 'filesystem'  
    SESSION_PERMANENT = False  
    SESSION_USE_SIGNER = True  
    SESSION_FILE_DIR = os.path.join(os.getcwd(), 'flask_session')
    @classmethod  
    def init_app_config(cls, app):  
        # Створення директорії для файлів сесії  
        if not os.path.exists(cls.SESSION_FILE_DIR):  
            os.makedirs(cls.SESSION_FILE_DIR)
            
    logging.basicConfig(  
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s',  
    handlers=[  
        logging.FileHandler('app.log'),  
        logging.StreamHandler()  
    ]  
)  