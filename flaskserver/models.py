from datetime import datetime

from sqlalchemy import null
from flaskserver import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    calendarEvents = db.relationship('CalendarEvent', backref='user', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

class CalendarEvent(db.Model):
    id_calendar = db.Column(db.Integer, primary_key=True)
    id_event = db.Column(db.Integer, db.ForeignKey('event.id_event'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    tag = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(10))
    description = db.Column(db.String(1000))
    startDate = db.Column(db.DateTime, default = datetime.utcnow)
    endDate = db.Column(db.DateTime, default=datetime.utcnow)
        
    def __repr__(self):
        return f"Event('{self.id_calendar}', '{self.id_event}', {self.title}', '{self.tag}', '{self.priority}', '{self.location}', '{self.description}', '{self.startDate}', '{self.endDate}')"

class Event(db.Model):
    id_event = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    calendarEvents = db.relationship('CalendarEvent', cascade="all, delete", backref='event', lazy=True)

db.create_all()