from extensions import db 
from sqlalchemy import Numeric  # Змінено імпорт  
from datetime import datetime 

class Tariff(db.Model):  
    __tablename__ = 'tariffs'  

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  
    description = db.Column(db.Text, nullable=True)  
    price = db.Column(Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):  
        return f'<Tariff {self.name}>'