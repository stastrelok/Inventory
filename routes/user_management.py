from flask import Blueprint, render_template, redirect, url_for, flash  
from flask_login import login_required, current_user  
from models.user import User  
from forms.user_form import UserForm  
from extensions import db  
from sqlalchemy.exc import IntegrityError  # Додайте імпорт для обробки помилок бази даних  

user_management_bp = Blueprint('user_management_routes', __name__, url_prefix='/admin/users')  

@user_management_bp.route('/', methods=['GET'])  
@login_required  
def user_list():  
    users = User.query.all()  
    return render_template('user_management/user_list.html', users=users)  

@user_management_bp.route('/add', methods=['GET', 'POST'])  
@login_required  
def add_user():  
    form = UserForm()  
    if form.validate_on_submit():  
        try:  
            # Перевірка на існування користувача  
            existing_user = User.query.filter(  
                (User.username == form.username.data) |   
                (User.email == form.email.data)  
            ).first()  
            
            if existing_user:  
                if existing_user.username == form.username.data:  
                    flash('Користувач з таким ім\'ям вже існує', 'danger')  
                else:  
                    flash('Користувач з такою електронною поштою вже існує', 'danger')  
                return render_template('user_management/user_form.html', form=form)  
            
            # Створення нового користувача  
            new_user = User(  
                username=form.username.data,  
                email=form.email.data,  
                role=form.role.data,  
                is_active=form.is_active.data  
            )  
            
            # Встановлення паролю  
            if form.password.data:  
                new_user.set_password(form.password.data)  
             
            db.session.add(new_user)  
            db.session.commit()  
            
            flash("Користувача успішно додано.", "success")  
            return redirect(url_for('user_management_routes.user_list'))  
        
        except IntegrityError:  
            db.session.rollback()  
            flash("Помилка при додаванні користувача. Перевірте введені дані.", "danger")  
        except Exception as e:  
            db.session.rollback()  
            flash(f"Непередбачена помилка: {str(e)}", "danger")  
    
    return render_template('user_management/user_form.html', form=form)  

@user_management_bp.route('/edit/<int:id>', methods=['GET', 'POST'])  
@login_required  
def edit_user(id):  
    user = User.query.get_or_404(id)  
    form = UserForm(obj=user)  
    
    if form.validate_on_submit():  
        try:    
            existing_user = User.query.filter(  
                ((User.username == form.username.data) |   
                 (User.email == form.email.data)) &   
                (User.id != id)  
            ).first()  
            
            if existing_user:  
                if existing_user.username == form.username.data:  
                    flash('Користувач з таким ім\'ям вже існує', 'danger')  
                else:  
                    flash('Користувач з такою електронною поштою вже існує', 'danger')  
                return render_template('user_management/user_form.html', form=form, user=user)  
             
            user.username = form.username.data  
            user.email = form.email.data  
            user.role = form.role.data  
            user.is_active = form.is_active.data  

            if form.password.data:  
                user.set_password(form.password.data)  
            
            db.session.commit()  
            flash("Дані користувача успішно оновлено.", "success")  
            return redirect(url_for('user_management_routes.user_list'))  
        
        except IntegrityError:  
            db.session.rollback()  
            flash("Помилка при оновленні користувача. Перевірте введені дані.", "danger")  
        except Exception as e:  
            db.session.rollback()  
            flash(f"Непередбачена помилка: {str(e)}", "danger")  
    
    return render_template('user_management/user_form.html', form=form, user=user)  

@user_management_bp.route('/delete/<int:id>', methods=['POST'])  
@login_required  
def delete_user(id):  
    user = User.query.get_or_404(id)  
    
    try:  
        db.session.delete(user)  
        db.session.commit()  
        flash("Користувача видалено.", "success")  
    except Exception as e:  
        db.session.rollback()  
        flash(f"Помилка при видаленні користувача: {str(e)}", "danger")  
    
    return redirect(url_for('user_management_routes.user_list'))
def user_list():
    users = User.query.order_by(User.username).all()
    return render_template('user_management/user_list.html', users=users)

@user_management_bp.route('/toggle-active/<int:id>', methods=['POST'])
@login_required
def toggle_active(id):
    if id == current_user.id:
        flash('Ви не можете деактивувати власний обліковий запис.', 'danger')
        return redirect(url_for('user_management_routes.user_list'))

    user = User.query.get_or_404(id)
    try:
        user.is_active = not user.is_active
        db.session.commit()
        status = "активовано" if user.is_active else "деактивовано"
        flash(f'Користувача {user.username} було успішно {status}.', 'success')
        log_action(f'Адміністратор {current_user.username} змінив статус is_active на {user.is_active} для користувача {user.username} (ID: {user.id})')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error toggling active status for user {id}: {e}", exc_info=True)
        flash('Не вдалося змінити статус користувача.', 'danger')

    return redirect(url_for('user_management_routes.user_list'))