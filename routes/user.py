from flask import Blueprint, render_template, redirect, url_for, flash  
from flask_login import login_required, current_user  
from models.user import User  
from forms.user import UserForm  
from extensions import db  

user_bp = Blueprint('user', __name__)  

@user_bp.route('/user/add', methods=['GET', 'POST'])  
@login_required  
def add_user():  
    if not current_user.is_admin:   
        flash('Недостатньо прав для цієї операції')  
        return redirect(url_for('some_view'))  

    form = UserForm()  
    
    if form.validate_on_submit():  
        try:  
            User.add_user(form.username.data, form.role.data) 
            Log.log_change('Додавання користувача', f'Користувач {form.username.data} доданий', current_user)
            flash('Користувача успішно додано')  
            return redirect(url_for('user.list'))  
        except Exception as e:  
            flash('Помилка при додаванні користувача: ' + str(e))  
    logs = Log.query.order_by(Log.created_at.desc()).all()
    return render_template('user_form.html', form=form) 