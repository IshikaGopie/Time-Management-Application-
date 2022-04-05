from datetime import datetime
from flaskserver import db

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    events = db.relationship('CalendarEvent', backref='id_user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}'"

class CalendarEvent(db.Model):
    id_calendar = db.Column(db.Integer, primary_key=True)
    id_event = db.Column(db.Integer, db.ForeignKey('event.id_event'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    tag = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(10))
    location = db.Column(db.String(10))
    description = db.Column(db.String(1000))
    startDate = db.Column(db.DateTime, default = datetime.utcnow)
    endDate = db.Column(db.DateTime)

    def __repr__(self):
        return f"Event('{self.title}', '{self.tag}', '{self.priority}', '{self.location}', '{self.description}', '{self.startDate}', '{self.endDate}'"

class Event(db.Model):
    id_event = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    calendarEvents = db.relationship('Event', backref='id_event', lazy=True)

db.create_all()