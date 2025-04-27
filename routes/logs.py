from flask import Blueprint, render_template  
from flask_login import login_required  
from models.log import Log  
from utils import admin_required  

logs_bp = Blueprint('logs', __name__)  

@logs_bp.route('/logs')  
@login_required  
@admin_required  
def view():  
    logs = Log.query.order_by(Log.created_at.desc()).all()  
    return render_template('logs.html', logs=logs)