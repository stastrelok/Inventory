from flask import Blueprint, render_template, redirect, url_for, flash, request  
from flask_login import login_required  
from models.street import Street  
from forms.street import StreetForm  
from extensions import db  
from utils import admin_required, log_action  

street_bp = Blueprint('street', __name__)  

@street_bp.route('/streets')  
@login_required  
def list():  
    streets = Street.query.all()  
    return render_template('street_list.html', streets=streets)  

@street_bp.route('/street/add', methods=['GET', 'POST'])  
@login_required  
@admin_required  
def add():  
    form = StreetForm()  
    if form.validate_on_submit():  
        street = Street(name=form.name.data)  
        db.session.add(street)  
        try:  
            db.session.commit()  
            log_action(f'Додано нову вулицю: {street.name}')  
            flash('Вулицю успішно додано')  
            return redirect(url_for('street.list'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Помилка при додаванні вулиці')  
    return render_template('street_form.html', form=form)  

@street_bp.route('/street/<int:id>/edit', methods=['GET', 'POST'])  
@login_required  
@admin_required  
def edit(id):  
    street = Street.query.get_or_404(id)  
    form = StreetForm(obj=street)  
    
    if form.validate_on_submit():  
        street.name = form.name.data  
        try:  
            db.session.commit()  
            log_action(f'Відредаговано вулицю: {street.name}')  
            flash('Вулицю успішно оновлено')  
            return redirect(url_for('street.list'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Помилка при оновленні вулиці')  
    
    return render_template('street_form.html', form=form, street=street)  

@street_bp.route('/street/<int:id>/delete', methods=['POST'])  
@login_required  
@admin_required  
def delete(id):  
    street = Street.query.get_or_404(id)  
    try:  
        db.session.delete(street)  
        db.session.commit()  
        log_action(f'Видалено вулицю: {street.name}')  
        flash('Вулицю успішно видалено')  
    except Exception as e:  
        db.session.rollback()  
        flash('Помилка при видаленні вулиці')  
    return redirect(url_for('street.list'))