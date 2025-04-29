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
from sqlalchemy import or_

client_bp = Blueprint('client', __name__, url_prefix='/clients')

@client_bp.route('/', methods=['GET'])
@login_required
def list_clients():

    query = Client.query

    search_query = request.args.get('search', '').strip()
    street_id = request.args.get('street', type=int)
    tariff_id = request.args.get('tariff', type=int)

    if search_query:
        
        query = query.filter(or_(
            Client.uid.ilike(f'%{search_query}%'),
            Client.full_name.ilike(f'%{search_query}%')
        ))

    if street_id:
        query = query.filter(Client.street_id == street_id)

    if tariff_id:
        query = query.filter(Client.tariff_id == tariff_id)

    clients = query.order_by(Client.created_at.desc()).all()
    streets = Street.query.order_by(Street.name).all()
    tariffs = Tariff.query.order_by(Tariff.name).all()

    return render_template('client/client_list.html',
                         clients=clients,
                         streets=streets,
                         tariffs=tariffs,
                         
                         search_query=search_query,
                         selected_street=street_id,
                         selected_tariff=tariff_id)

@client_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_client():
    if current_user.role not in ['admin', 'user']:
        flash('Недостатньо прав для цієї операції', 'warning')
        return redirect(url_for('client.list_clients'))

    form = ClientForm()
    form.street_id.choices = [(s.id, s.name) for s in Street.query.order_by(Street.name).all()]
    form.tariff_id.choices = [(t.id, t.name) for t in Tariff.query.order_by(Tariff.name).all()]

    available_equipment = [(e.id, f"{e.manufacturer} {e.model} (SN: {e.serial_number})")
                           for e in Equipment.query.filter_by(status='available').order_by(Equipment.manufacturer, Equipment.model).all()]
    form.equipment_id.choices = [(0, "--- Відсутнє ---")] + available_equipment
    form.equipment_id.coerce = int

    if form.validate_on_submit():
        selected_equipment_id = form.equipment_id.data
        equipment_to_assign = None

        if selected_equipment_id and selected_equipment_id != 0:
            equipment_to_assign = Equipment.query.filter_by(id=selected_equipment_id, status='available').first()
            if not equipment_to_assign:
                flash("Вибране обладнання недоступне або не існує.", "danger")
                form.street_id.choices = [(s.id, s.name) for s in Street.query.order_by(Street.name).all()]
                form.tariff_id.choices = [(t.id, t.name) for t in Tariff.query.order_by(Tariff.name).all()]
                form.equipment_id.choices = [(0, "--- Відсутнє ---")] + available_equipment
                return render_template('client/client_form.html', form=form, title="Додати клієнта")

        new_client = Client(
            uid=form.uid.data,
            full_name=form.full_name.data,
            street_id=form.street_id.data,
            house_number=form.house_number.data,
            apartment=form.apartment.data,
            tariff_id=form.tariff_id.data,
            user_id=current_user.id,
            equipment_id=equipment_to_assign.id if equipment_to_assign else None
        )

        try:
            db.session.add(new_client)

            if equipment_to_assign:
                equipment_to_assign.status = 'in_use'
                equipment_to_assign.client_id = new_client.id
                db.session.add(equipment_to_assign)

            log_detail = f'Client UID: {new_client.uid}, Name: {new_client.full_name}'
            if equipment_to_assign:
                log_detail += f', Equipment ID: {equipment_to_assign.id}'
            log_action('CREATE_CLIENT', log_detail)

            db.session.commit()

            flash('Клієнта успішно додано', 'success')
            return redirect(url_for('client.list_clients'))

        except Exception as e:
            db.session.rollback()
            logging.error(f"Помилка при додаванні клієнта: {e}", exc_info=True)
            flash('Помилка при додаванні клієнта. Зверніться до адміністратора.', 'danger')

    return render_template('client/client_form.html', form=form, title="Додати клієнта")


@client_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_client(id):
    client = Client.query.get_or_404(id)
    original_equipment_id = client.equipment_id

    form = ClientForm(obj=client)
    form.street_id.choices = [(s.id, s.name) for s in Street.query.order_by(Street.name).all()]
    form.tariff_id.choices = [(t.id, t.name) for t in Tariff.query.order_by(Tariff.name).all()]

    available_equipment_query = Equipment.query.filter_by(status='available')
    current_equipment = Equipment.query.get(original_equipment_id) if original_equipment_id else None
    equipment_choices = [(0, "--- Відсутнє ---")]
    if current_equipment:

        equipment_choices.append((current_equipment.id, f"{current_equipment.manufacturer} {current_equipment.model} (SN: {current_equipment.serial_number}) - ПОТОЧНЕ"))
        available_equipment_query = available_equipment_query.filter(Equipment.id != current_equipment.id)

    equipment_choices.extend([(e.id, f"{e.manufacturer} {e.model} (SN: {e.serial_number})")
                              for e in available_equipment_query.order_by(Equipment.manufacturer, Equipment.model).all()])

    form.equipment_id.choices = equipment_choices
    form.equipment_id.coerce = int

    if form.validate_on_submit():
        new_equipment_id = form.equipment_id.data if form.equipment_id.data != 0 else None
        equipment_to_assign = None
        equipment_to_release = None

        if original_equipment_id and original_equipment_id != new_equipment_id:
            equipment_to_release = Equipment.query.get(original_equipment_id)

        if new_equipment_id and new_equipment_id != original_equipment_id:
            equipment_to_assign = Equipment.query.filter_by(id=new_equipment_id, status='available').first()
            if not equipment_to_assign:
                flash("Вибране нове обладнання недоступне або не існує.", "danger")
                form.street_id.choices = [(s.id, s.name) for s in Street.query.order_by(Street.name).all()]
                form.tariff_id.choices = [(t.id, t.name) for t in Tariff.query.order_by(Tariff.name).all()]
                form.equipment_id.choices = equipment_choices
                return render_template('client/client_form.html', form=form, client=client, title="Редагувати клієнта")

        client.uid = form.uid.data
        client.full_name = form.full_name.data
        client.street_id = form.street_id.data
        client.house_number = form.house_number.data
        client.apartment = form.apartment.data
        client.tariff_id = form.tariff_id.data
        client.equipment_id = new_equipment_id
        client.user_id = current_user.id

        try:
            db.session.add(client)

            if equipment_to_release:
                equipment_to_release.status = 'available'
                equipment_to_release.client_id = None
                db.session.add(equipment_to_release)
            if equipment_to_assign:
                equipment_to_assign.status = 'in_use'
                equipment_to_assign.client_id = client.id
                db.session.add(equipment_to_assign)

            log_detail = f'Client ID: {client.id}, UID: {client.uid}, Name: {client.full_name}'
            if original_equipment_id != new_equipment_id:
                 log_detail += f'. Equipment changed from {original_equipment_id or "None"} to {new_equipment_id or "None"}'
            log_action('UPDATE_CLIENT', log_detail)

            db.session.commit()

            flash('Дані клієнта успішно оновлено', 'success')
            return redirect(url_for('client.list_clients'))

        except Exception as e:
            db.session.rollback()
            logging.error(f"Помилка при оновленні клієнта ID {id}: {e}", exc_info=True)
            flash('Помилка при оновленні даних клієнта.', 'danger')

    if request.method == 'GET':
        form.equipment_id.data = original_equipment_id if original_equipment_id else 0

    return render_template('client/client_form.html', form=form, client=client, title="Редагувати клієнта")


@client_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_client(id):
    client = Client.query.get_or_404(id)
    equipment_to_release = None
    client_name = client.full_name # Зберігаємо для логу

    if client.equipment_id:
        equipment_to_release = Equipment.query.get(client.equipment_id)

    try:
        if equipment_to_release:
            equipment_to_release.status = 'available'
            equipment_to_release.client_id = None
            db.session.add(equipment_to_release)

        db.session.delete(client)

        log_detail = f'Client ID: {id}, Name: {client_name}'
        if equipment_to_release:
            log_detail += f', Released Equipment ID: {equipment_to_release.id}'
        log_action('DELETE_CLIENT', log_detail)

        db.session.commit()

        flash(f'Клієнта "{client_name}" успішно видалено.', 'success')

    except Exception as e:
        db.session.rollback()
        logging.error(f"Помилка при видаленні клієнта ID {id}: {e}", exc_info=True)
        flash('Помилка при видаленні клієнта.', 'danger')

    return redirect(url_for('client.list_clients'))