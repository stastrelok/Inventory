from extensions import db  # Змінено імпорт  
from sqlalchemy import Column, Integer, String, ForeignKey, Date  
from sqlalchemy.orm import relationship  
from datetime import datetime
from .equipment import Equipment

class Client(db.Model):  
    __tablename__ = 'clients'  

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)   
    street_id = db.Column(db.Integer, db.ForeignKey('streets.id'), nullable=False)  
    street = db.relationship('Street', backref='clients')
    house_number = db.Column(db.String(10), nullable=False)  
    apartment = db.Column(db.String(10), nullable=True)   
    tariff_id = db.Column(db.Integer, db.ForeignKey('tariffs.id'), nullable=False) 
    tariff = db.relationship('Tariff', backref='clients') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)  
    user = relationship("User", backref="clients")  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    equipments = db.relationship('Equipment', foreign_keys=[Equipment.client_id])
    
    def __repr__(self):  
        return f'<Client {self.full_name}>'