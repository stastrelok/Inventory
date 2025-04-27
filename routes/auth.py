from flask import Blueprint, render_template, redirect, url_for, flash, request, session  
from flask_login import login_user, logout_user, login_required, current_user  
from werkzeug.security import check_password_hash  
from models.user import User  
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email
from forms.auth import LoginForm, RegistrationForm  
from extensions import db, migrate, login_manager, csrf  
from utils import log_action  
import logging
import secrets

auth_bp = Blueprint('auth', __name__)  

@auth_bp.route('/login', methods=['GET', 'POST'])  
def login():  
    if '_id' not in session:  
        session['_id'] = secrets.token_hex(16)
    if current_user.is_authenticated:  
        return redirect(url_for('main.index'))
    if request.method == 'GET':  
        next_page = request.args.get('next')  
        if next_page:  
            return redirect(next_page)  
            
    form = LoginForm()  
    logging.info(f"CSRF token in form: {form.csrf_token.current_token}")  
    logging.info(f"Session contains csrf_token: {'csrf_token' in session}")
    logging.debug(f"Session contents on GET/POST: {dict(session)}")
    
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()

            if user and check_password_hash(user.password_hash, form.password.data):
                 #if not user.is_active:
                  #  flash('Ваш акаунт деактивовано. Зверніться до адміністратора.', 'warning')
                  #  return redirect(url_for('auth.login'))
                    login_user(user)
                    next_page = request.args.get('next')
                    flash('Вхід виконано успішно!', 'success')
                    if next_page and (not next_page.startswith('/') or next_page.startswith('//') or next_page.startswith('http')):
                     next_page = url_for('main.index') # Or handle safely
                    return redirect(next_page or url_for('main.index'))
            else:
                flash('Невірний email або пароль', 'danger')
        except Exception as e:
            logging.error(f"Login error: {e}", exc_info=True) # Log traceback
            flash('Сталася помилка під час входу. Спробуйте ще раз.', 'danger')
    elif request.method == 'POST':
         logging.warning(f"Form validation failed: {form.errors}")
    return render_template('login.html', form=form) 

@auth_bp.route('/logout')  
@login_required  
def logout():  
    log_action(f'Користувач {current_user.username} вийшов з системи')  
    logout_user() 
    flash('Ви успішно вийшли з системи.')
    return redirect(url_for('main.index'))  

@auth_bp.route('/register', methods=['GET', 'POST'])  
def register():  
    if not User.query.first():  
        form = RegistrationForm()  
        if form.validate_on_submit():  
            user = User(  
                username=form.username.data,  
                email=form.email.data,  
                is_admin=True,
                is_active=True
            )  
            user.set_password(form.password.data)  
            db.session.add(user)  
            try:  
                db.session.commit()  
                log_action('Створено першого адміністратора системи')  
                flash('Реєстрація успішна! Тепер ви можете увійти.')  
                return redirect(url_for('auth.login'))  
            except Exception as e:  
                db.session.rollback()  
                flash('Помилка при реєстрації')  
        return render_template('register.html', form=form)  
    flash('Реєстрація заборонена')  
    return redirect(url_for('main.index'))