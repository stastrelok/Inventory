from extensions import db, migrate, login_manager  
from flask_login import UserMixin  
from werkzeug.security import generate_password_hash, check_password_hash  
from sqlalchemy.exc import IntegrityError  
from datetime import datetime
import logging

class User(UserMixin, db.Model):  
    __tablename__ = 'users'  

    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(50), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(255), nullable=False)  
    role = db.Column(db.Enum('admin', 'user', 'guest'), default='guest', nullable=False)  
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False, server_default='1')  
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
     
    def set_password(self, password):  
        self.password_hash = generate_password_hash(password)  
        if not password:
            logging.error("Attempted to set an empty password.")
            raise ValueError("Password cannot be empty.")
        self.password_hash = generate_password_hash(password)
        logging.debug(f"Password hash set for user {self.username}")
    def check_password(self, password):  
        if not self.password_hash:
            logging.warning(f"User {self.username} has no password hash set.")
            return False
        if not password:
            logging.warning(f"Attempted to check an empty password for user {self.username}")
            return False
        return check_password_hash(self.password_hash, password)  
    
    @property  
    def is_admin(self):  
        return self.role == 'admin'  

    @property  
    def is_user(self):  
        return self.role == 'user'  

    @staticmethod  
    def add_user(username, email, password, role='guest'):    
        valid_roles = ['admin', 'user', 'guest']  
        if role not in valid_roles:  
            role = 'guest'    

        existing_user = User.query.filter(  
            (User.username == username) | (User.email == email)  
        ).first()  
        
        if existing_user:  
            raise ValueError("Користувач з таким ім'ям або електронною поштою вже існує")  
        
        new_user = User(  
            username=username,   
            email=email,   
            role=role,  
            is_active=True  
        )  
        new_user.set_password(password)  
        db.session.add(new_user)  
        
        try:  
            db.session.commit()  
            return new_user  
        except Exception as e:  
            db.session.rollback()  
            raise ValueError(f"Помилка створення користувача: {str(e)}")