from extensions import db 
from datetime import datetime  

class Equipment(db.Model):  
    __tablename__ = 'equipment'  

    id = db.Column(db.Integer, primary_key=True)  
    manufacturer = db.Column(db.String(100), nullable=False)  
    model = db.Column(db.String(100), nullable=False)  
    serial_number = db.Column(db.String(100), unique=True, nullable=False)  
    mac_address = db.Column(db.String(17), unique=True)  
    status = db.Column(db.Enum('in_use', 'available', 'written_off'), default='available')  
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  
    written_off_at = db.Column(db.DateTime)
    is_used = db.Column(db.Boolean, default=False)    

    client = db.relationship('Client', foreign_keys=[client_id], back_populates='equipments')