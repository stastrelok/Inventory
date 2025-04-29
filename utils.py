# utils.py
from flask import current_app, request, redirect, url_for, flash # Додав flash для admin_required
from extensions import db
from models.log import Log
from flask_login import current_user
from datetime import datetime
from functools import wraps
import logging

# Декоратор admin_required залишається без змін

def log_action(action_description, detail="N/A"):
    """Додає запис логу до поточної сесії бази даних."""
    # !!! ВАЖЛИВО: Ця функція не робить commit або rollback !!!
    try:
        if not current_user or not current_user.is_authenticated:
             # Якщо логування для неавтентифікованих дій не потрібне або
             # user_id в Log може бути NULL, то можна просто повернути:
             # return
             # Або встановити user_id в None, якщо поле Log.user_id це дозволяє
             user_id = None
             username = 'System/Anonymous'
        else:
             user_id = current_user.id
             username = current_user.username # Переконайтесь, що у моделі User є поле username

        # Отримання IP-адреси - обережно за проксі!
        # request.remote_addr може бути IP проксі. Для реальних додатків
        # часто дивляться на заголовки типу X-Forwarded-For, але це вимагає
        # довіри до конфігурації проксі. Для простоти залишимо remote_addr.
        ip_address = request.remote_addr if request else 'Unknown'

        log_entry = Log(
            created_at=datetime.utcnow(),
            action=action_description,
            detail=detail,
            user_id=user_id, # Переконайтесь, що модель Log дозволяє user_id=None, якщо потрібно
            # Додайте поля ip_address та username до моделі Log, якщо їх там ще немає
            # ip_address=ip_address,
            # username=username
        )
        db.session.add(log_entry)
        logging.debug(f"Запис логу '{action_description}' додано до сесії.")

    except Exception as e:
        logging.error(f"Помилка при підготовці запису логу '{action_description}': {e}", exc_info=True)