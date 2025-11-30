import numpy as np
import joblib
from datetime import datetime, timedelta
from app.models.workout import Workout, db
class AIService:
	def __init__(self, model_path='app/ai/model.pkl'):
		self.model = joblib.load(model_path)
		self.exercise_database = self._load_exercises()

	def _load_exercises(self):
		"""Wczytuje dostępne ćwiczenia z bazy danych"""
		exercises = {
			'low_intensity': [
				{'name': 'Pompki (modyfikowane)', 'sets': 3, 'reps': 8, 'category': 'ches'},
				{'name': 'Przysiady bez obciążenia', 'sets': 3, 'reps': 10, 'category': ''},
				{'name': 'Rozciąganie', 'duration': '10 min', 'category': 'recovery'}
			],
			'medium_intensity': [
				{'name': 'Wyciskanie sztangi', 'sets': 4, 'reps': 10, 'weight': '70% RM'},
				{'name': 'Przysiady ze sztangą', 'sets': 4, 'reps': 8, 'weight': '75% RM'},
				{'name': 'Wiosłowanie', 'sets': 3, 'reps': 12, 'category': 'back'}
			],
			'high_intensity': [
				{'name': 'Wyciskanie sztangi', 'sets': 5, 'reps': 5, 'weight': '85% RM'},
				{'name': 'Martwy ciąg', 'sets': 5, 'reps': 5, 'weight': '85% RM', 'category': ''},
				{'name': 'Przysiady ze sztangą', 'sets': 5, 'reps': 5, 'weight': '85% RM'}
			]
		}
		return exercises

	def extract_features(self, user_id, fatigue, stress, motivation):
		"""Ekstrakcja cech do modelu ML"""
		# Pobieranie historii treningów
		recent_workouts = Workout.query.filter_by(user_id=user_id)\
			.order_by(Workout.date.desc()).limit(10).all()
		avg_intensity = np.mean([w.intensity for w in recent_workouts]) if recent_workouts else 0
		days_since_last = (datetime.utcnow() - recent_workouts[0].date).days if recent_workouts else 0
		# Normalizacja cech do zakresu 0-1
		features = np.array([[
			fatigue / 10.0,
			stress / 10.0,
			motivation / 10.0,
			avg_intensity / 100.0,
			min(days_since_last / 7.0, 1.0) # Maksimum 1.0 dla 7+ dni
		]])
		return features

	def predict_intensity(self, user_id, fatigue, stress, motivation):
		"""Predykcja intensywności treningu"""
		features = self.extract_features(user_id, fatigue, stress, motivation)
		intensity = self.model.predict(features)[0]
		# Mapowanie wyniku (0-100)
		intensity_score = max(0, min(100, intensity * 100))
		return intensity_score

	def generate_workout_plan(self, intensity_score):
		"""Generowanie planu treningowego na podstawie intensywności"""
		if intensity_score < 30:
			return {
				'type': 'Trening regeneracyjny',
				'intensity': intensity_score,
				'exercises': self.exercise_database['low_intensity']
			}
		elif intensity_score < 70:
			return {
				'type': 'Trening standardowy',
				'intensity': intensity_score,
				'exercises': self.exercise_database['medium_intensity']
			}
		else:
			return {
				'type': 'Trening intensywny',
				'intensity': intensity_score,
				'exercises': self.exercise_database['high_intensity']
			}