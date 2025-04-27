from extensions import db 
from datetime import datetime  

class Street(db.Model):  
    __tablename__ = 'streets'  

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), unique=True, nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)