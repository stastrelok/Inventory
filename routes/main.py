from flask import Blueprint, render_template  
from flask_login import login_required  
from models.equipment import Equipment  
from models.client import Client

main_bp = Blueprint('main', __name__)  

@main_bp.route('/')
def index():  
    total_equipment = Equipment.query.count()  
    in_use_equipment = Equipment.query.filter_by(status='in_use').count()  
    available_equipment = Equipment.query.filter_by(status='available').count()  
    written_off_equipment = Equipment.query.filter_by(status='written_off').count()  
    recent_clients = Client.query.order_by(Client.created_at.desc()).limit(5).all()
    all_equipment = Equipment.query.all()
 
    return render_template('index.html',  
                         total_equipment=total_equipment,  
                         in_use_equipment=in_use_equipment,  
                         available_equipment=available_equipment,  
                         written_off_equipment=written_off_equipment,  
                         recent_clients=recent_clients,
                         all_equipment=all_equipment)