from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
db = SQLAlchemy()
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	# Relacje
	mood_logs = db.relationship('MoodLog', backref='user', lazy=True, cascade='all, delete')
	workouts = db.relationship('Workout', backref='user', lazy=True, cascade='all, delete')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def to_dict(self):
		return {
			'id': self.id,
			'email': self.email,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'created_at': self.created_at.isoformat()
		}

class MoodLog(db.Model):
	__tablename__ = 'mood_logs'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	fatigue = db.Column(db.Integer, nullable=False) # 1-10
	stress = db.Column(db.Integer, nullable=False) # 1-10
	motivation = db.Column(db.Integer, nullable=False) # 1-10
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	notes = db.Column(db.Text, nullable=True)

	def to_dict(self):
		return {
			'id': self.id,
			'user_id': self.user_id,
			'fatigue': self.fatigue,
			'stress': self.stress,
			'motivation': self.motivation,
			'timestamp': self.timestamp.isoformat(),
			'notes': self.notes
		}

class Workout(db.Model):
	__tablename__ = 'workouts'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	mood_log_id = db.Column(db.Integer, db.ForeignKey('mood_logs.id'))
	workout_type = db.Column(db.String(100), nullable=False)
	intensity = db.Column(db.Float, nullable=False) # 0-100
	exercises = db.Column(db.JSON, nullable=False) # Przechowuje listę ćwiczeń
	completed = db.Column(db.Boolean, default=False)
	date = db.Column(db.DateTime, default=datetime.utcnow)

	def to_dict(self):
		return {
			'id': self.id,
			'user_id': self.user_id,
			'workout_type': self.workout_type,
			'intensity': self.intensity,
			'exercises': self.exercises,
			'completed': self.completed,
			'date': self.date.isoformat()
		}