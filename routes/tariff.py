from flask import Blueprint, render_template, redirect, url_for, flash, request  
from flask_login import login_required  
from models.tariff import Tariff  
from forms.tariff import TariffForm  
from extensions import db 
from utils import admin_required, log_action  

tariff_bp = Blueprint('tariff', __name__)  

@tariff_bp.route('/tariffs')  
@login_required  
def list():  
    tariffs = Tariff.query.all()  
    return render_template('tariff_list.html', tariffs=tariffs)  

@tariff_bp.route('/tariff/add', methods=['GET', 'POST'])  
@login_required  
@admin_required  
def add():  
    form = TariffForm()  
    if form.validate_on_submit():  
        tariff = Tariff(  
            name=form.name.data,  
            price=form.price.data,  
            description=form.description.data  
        )  
        db.session.add(tariff)  
        try:  
            db.session.commit()  
            log_action(f'Додано новий тариф: {tariff.name}')  
            flash('Тариф успішно додано')  
            return redirect(url_for('tariff.list'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Помилка при додаванні тарифу')  
    return render_template('tariff_form.html', form=form)  

@tariff_bp.route('/tariff/<int:id>/edit', methods=['GET', 'POST'])  
@login_required  
@admin_required  
def edit(id):  
    tariff = Tariff.query.get_or_404(id)  
    form = TariffForm(obj=tariff)  
    
    if form.validate_on_submit():  
        tariff.name = form.name.data  
        tariff.price = form.price.data  
        tariff.description = form.description.data  
        
        try:  
            db.session.commit()  
            log_action(f'Відредаговано тариф: {tariff.name}')  
            flash('Тариф успішно оновлено')  
            return redirect(url_for('tariff.list'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Помилка при оновленні тарифу')  
    
    return render_template('tariff_form.html', form=form, tariff=tariff)  

@tariff_bp.route('/tariff/<int:id>/delete', methods=['POST'])  
@login_required  
@admin_required  
def delete(id):  
    tariff = Tariff.query.get_or_404(id)  
    try:  
        db.session.delete(tariff)  
        db.session.commit()  
        log_action(f'Видалено тариф: {tariff.name}')  
        flash('Тариф успішно видалено')  
    except Exception as e:  
        db.session.rollback()  
        flash('Помилка при видаленні тарифу')  
    return redirect(url_for('tariff.list'))