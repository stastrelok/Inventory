from flask import current_app, request, redirect, url_for
from extensions import db
from models.log import Log  
from flask_login import current_user  
from datetime import datetime
from functools import wraps 
import logging
 

def admin_required(f):  
    @wraps(f)  
    def decorated_function(*args, **kwargs):  
        if not current_user.is_admin:  
            flash('Ця дія доступна лише адміністраторам.', 'danger')
            return redirect(url_for('main.index'))  
        return f(*args, **kwargs)  
    
    return decorated_function 

def log_action(action_description, detail="N/A"):  
 
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        ip_address = request.remote_addr if request else 'Unknown'

        log_entry = Log(
            created_at=datetime.utcnow(),
            action=action_description,
            detail=detail,
            user_id=user_id,
            ip_address=ip_address,
            username=current_user.username if user_id else 'System/Anonymous'
        )
        db.session.add(log_entry)
        db.session.commit()
        logging.debug(f"Логування успішне: {action_description}")

    except Exception as e:
        logging.error(f"Помилка логування '{action_description}': {e}", exc_info=True)
        db.session.rollback()
