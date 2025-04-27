from flask import Blueprint, render_template, redirect, url_for, flash, request  
from flask_login import login_required, current_user  
from models.client import Client  
from models.street import Street  
from models.tariff import Tariff  
from models.equipment import Equipment
from forms.client import ClientForm, FilterForm 
from extensions import db  
from utils import admin_required, log_action 
import logging 

client_bp = Blueprint('client', __name__)  

@client_bp.route('/clients', methods=['GET'])  
@login_required  
def list(): 
    form = FilterForm()
    clients = Client.query
    search_query = request.args.get('search')  
    street_id = request.args.get('street')  
    tariff_id = request.args.get('tariff')  
 
    if search_query:  
        clients = clients.filter((Client.uid.like(f'%{search_query}%')) | (Client.full_name.like(f'%{search_query}%')))  
 
    if street_id:  
        clients = clients.filter(Client.street_id == street_id)  
 
    if tariff_id:  
        clients = clients.filter(Client.tariff_id == tariff_id)
        
    clients = clients.all()  # Додайте перевірку тут  
    print("Filtered Clients Count:", len(clients)) 
    
    if form.validate_on_submit():  
        filter_value = form.filter_field.data  
        clients = clients.filter(Client.field_name == filter_value) 

    clients = Client.query.all()  
    streets = Street.query.all()  
    tariffs = Tariff.query.all()  
    return render_template('client_list.html',   
                         clients=clients,   
                         streets=streets,   
                         tariffs=tariffs)  

@client_bp.route('/client/add', methods=['GET', 'POST'])  
@login_required  
def add():  
    if not (current_user.is_admin or current_user.is_user):  
        flash('Недостатньо прав для цієї операції')  
        return redirect(url_for('client.list'))  

    form = ClientForm()  
    form.street_id.choices = [(s.id, s.name) for s in Street.query.all()]  
    form.tariff_id.choices = [(t.id, t.name) for t in Tariff.query.all()]  
    form.equipment_id.choices = [(None, "Відсутнє")] + [(e.id, f"{e.manufacturer} - {e.model}") for e in Equipment.query.filter_by(is_used=False).all()]   

    if form.validate_on_submit(): 
             
        existing_client = None
        if form.equipment_id.data: 
            equipment = Equipment.query.get(form.equipment_id.data)  
            if equipment:  
                equipment.is_used = True  
            else:  
                flash("Обладнання не знайдено.", "error")  
                return redirect(url_for('client.add'))  
        else:  
            flash("Виберіть обладнання.", "error")  
        if existing_client:  
            flash('Це обладнання вже призначене іншому клієнту.')  
            return redirect(url_for('client.list'))   
        
        client = Client(  
            uid=form.uid.data,  
            full_name=form.full_name.data,  
            street_id=form.street_id.data,  
            house_number=form.house_number.data,  
            apartment=form.apartment.data,  
            tariff_id=form.tariff_id.data,  
            equipment_id=form.equipment_id.data if form.equipment_id.data is not None else None  
        )  
        db.session.add(client)  
        try:  
            db.session.commit()  
            log_action(f'Додано нового клієнта: {client.full_name}')  
            flash('Клієнта успішно додано')  
            return redirect(url_for('client.list'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Помилка при додаванні клієнта')  
    
    return render_template('client_form.html', form=form)  

@client_bp.route('/client/<int:id>/edit', methods=['GET', 'POST'])  
@login_required  
@admin_required  
def edit(id):  
    client = Client.query.get_or_404(id)  
    form = ClientForm(obj=client)  
    form.street_id.choices = [(s.id, s.name) for s in Street.query.all()]  
    form.tariff_id.choices = [(t.id, t.name) for t in Tariff.query.all()]  
    form.equipment_id.choices = [(None, "Відсутнє")] + [(e.id, f"{e.manufacturer} - {e.model}") for e in Equipment.query.filter_by(is_used=False).all()]  
    
    if form.validate_on_submit():
        print(f"equipment_id data: {form.equipment_id.data}")    
        if form.equipment_id.data is not None:               
            form.equipment_id.data = None
            existing_client = Client.query.filter_by(equipment_id=form.equipment_id.data).first()  
            if existing_client and existing_client.id != client.id:
                flash('Це обладнання вже призначене іншому клієнту.')  
                return redirect(url_for('client.list'))   
            
        
        client.uid = form.uid.data  
        client.full_name = form.full_name.data  
        client.street_id = form.street_id.data  
        client.house_number = form.house_number.data  
        client.apartment = form.apartment.data  
        client.tariff_id = form.tariff_id.data  
        client.equipment_id = form.equipment_id.data if form.equipment_id.data is not None else None


        try:  
            db.session.commit()  
            log_action(f'Відредаговано клієнта: {client.full_name}')  
            flash('Дані клієнта успішно оновлено')  
            return redirect(url_for('client.list'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Помилка при оновленні даних клієнта')  
    
    return render_template('client_form.html', form=form, client=client)