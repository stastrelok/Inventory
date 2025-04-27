from flask import Flask, session, request  
from config import Config  
from extensions import db, migrate, login_manager, csrf  
from models.user import User
from flask_session import Session  
from flask_wtf.csrf import CSRFProtect   
from flask_login import LoginManager   
import pymysql  
import logging  
import os
import secrets

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s - %(levelname)s - %(message)s')  

pymysql.install_as_MySQLdb() 


login_manager = LoginManager()  
csrf = CSRFProtect() 
sess = Session()  

def create_app():  
    app = Flask(__name__)  
    app.config.from_object(Config) 
    Config.init_app_config(app)     
    # Ініціалізація розширень  
    db.init_app(app)  
    migrate.init_app(app, db)
    global csrf
    sess.init_app(app)
    csrf.init_app(app)  
    login_manager.init_app(app)  
    login_manager.login_view = 'auth.login'  
    login_manager.session_protection = "strong"   

    @login_manager.user_loader  
    def load_user(user_id):  
        return User.query.get(int(user_id))  
    
    # Реєстрація блюпринтів з перевіркою на наявність   
    blueprints = [  
        'routes.auth:auth_bp',  
        'routes.main:main_bp',  
        'routes.client:client_bp',  
        'routes.equipment:equipment_bp',  
        'routes.logs:logs_bp',  
        'routes.street:street_bp',  
        'routes.tariff:tariff_bp',  
        'routes.user:user_bp',  
        'routes.user_management:user_management_bp'  
    ]  

    for blueprint_path in blueprints:  
        try:  
            module_name, blueprint_name = blueprint_path.rsplit(':', 1)  
            module = __import__(module_name, fromlist=[blueprint_name])  
            blueprint = getattr(module, blueprint_name)  
            app.register_blueprint(blueprint)  
            logging.info(f"Successfully registered blueprint: {blueprint_path}")  
        except (ImportError, AttributeError) as e:  
            logging.error(f"Failed to register blueprint {blueprint_path}: {e}")  
    
    # Додаткова налагоджувальна інформація  
    @app.before_request  
    def before_request():  
        # Переконатися що сесія створена перед використанням CSRF  
        if not session.get('_id'):  
            session['_id'] = secrets.token_hex(16)
            session.modified = True
    
    @app.before_request  
    def log_request_info():  
        logging.debug(f'Request Headers: {request.headers}')  
        logging.debug(f'Request Path: {request.path}')  
    
    @app.after_request
    def log_session_after_request(response):
        logging.debug(f'Session Contents After Request: {dict(session)}')
        return response

    return app  

app = create_app()  

if __name__ == '__main__':  
    session_dir = app.config.get('SESSION_FILE_DIR', os.path.join(os.getcwd(), 'flask_session'))
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
        logging.info(f"Created session directory: {session_dir}")
    app.run(host='0.0.0.0', port=5000, debug=True)