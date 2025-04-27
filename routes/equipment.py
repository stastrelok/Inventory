from flask import Blueprint, render_template, redirect, url_for, flash, request  
from flask_login import login_required, current_user  
from models.equipment import Equipment  
from forms.equipment import EquipmentForm  
from extensions import db  
from utils import admin_required, log_action  

equipment_bp = Blueprint('equipment', __name__)  

@equipment_bp.route('/equipment')  
@login_required  
def list():  
    equipment = Equipment.query.all()  
    return render_template('equipment_list.html', equipment=equipment)  

@equipment_bp.route('/equipment/add', methods=['GET', 'POST'])  
@login_required  
def add():  
    if not (current_user.is_admin or current_user.is_user):  
        flash('Недостатньо прав для цієї операції')  
        return redirect(url_for('equipment.list'))  
    
    form = EquipmentForm()  
    if form.validate_on_submit():  
        equipment = Equipment(  
            manufacturer=form.manufacturer.data,  
            model=form.model.data,  
            serial_number=form.serial_number.data,  
            mac_address=form.mac_address.data,  
            status=form.status.data  
        )  
        db.session.add(equipment)  
        try:  
            db.session.commit()  
            log_action(f'Додано нове обладнання: {equipment.manufacturer} {equipment.model}')  
            flash('Обладнання успішно додано')  
            return redirect(url_for('equipment.list'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Помилка при додаванні обладнання')  
    return render_template('equipment_form.html', form=form)  

@equipment_bp.route('/equipment/<int:id>/edit', methods=['GET', 'POST'])  
@login_required  
@admin_required  
def edit(id):  
    equipment = Equipment.query.get_or_404(id)  
    form = EquipmentForm(obj=equipment)  
    
    if form.validate_on_submit():  
        equipment.manufacturer = form.manufacturer.data  
        equipment.model = form.model.data  
        equipment.serial_number = form.serial_number.data  
        equipment.mac_address = form.mac_address.data  
        equipment.status = form.status.data  
        
        try:  
            db.session.commit()  
            log_action(f'Відредаговано обладнання: {equipment.manufacturer} {equipment.model}')  
            flash('Обладнання успішно оновлено')  
            return redirect(url_for('equipment.list'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Помилка при оновленні обладнання')  
    
    return render_template('equipment_form.html', form=form, equipment=equipment)  

@equipment_bp.route('/equipment/<int:id>/delete', methods=['POST'])  
@login_required  
@admin_required  
def delete(id):  
    equipment = Equipment.query.get_or_404(id)  
    try:  
        db.session.delete(equipment)  
        db.session.commit()  
        log_action(f'Видалено обладнання: {equipment.manufacturer} {equipment.model}')  
        flash('Обладнання успішно видалено')  
    except Exception as e:  
        db.session.rollback()  
        flash('Помилка при видаленні обладнання')  
    return redirect(url_for('equipment.list'))