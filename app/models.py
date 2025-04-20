
from datetime import datetime, timezone
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    timezone = db.Column(db.String(50), default='UTC')
    apply_to_weekends = db.Column(db.Boolean, default=False)
    enable_notifications = db.Column(db.Boolean, default=True)
    notification_advance = db.Column(db.Integer, default=5)  
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    phases = db.relationship('Phase', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Phase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.String(5), nullable=False)  # Format: "HH:MM" in 24-hour
    end_time = db.Column(db.String(5), nullable=False)    # Format: "HH:MM" in 24-hour
    color = db.Column(db.String(20), default='#3498db')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"Phase('{self.name}', '{self.start_time}-{self.end_time}')"