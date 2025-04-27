from extensions import db  
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey  
from sqlalchemy.orm import relationship  
from datetime import datetime  

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    action = db.Column(db.Text, nullable=False) # Use Text for potentially long actions
    detail = db.Column(db.Text, nullable=True)  # Make detail nullable if not always needed
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Keep nullable
    username = db.Column(db.String(64), nullable=True) # Store username
    ip_address = db.Column(db.String(45), nullable=True) # Store IP (allow null if request context missing)

    def __repr__(self):
        return f'<Log {self.created_at} - {self.username or "System"} - {self.action[:50]}>'