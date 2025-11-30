from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User, db
from app.models.mood_log import MoodLog
from app.models.workout import Workout
from app.services.ai_service import AIService
from app.utils.decorators import validate_json
mood_bp = Blueprint('mood', __name__, url_prefix='/api/mood')
ai_service = AIService()
@mood_bp.route('', methods=['POST'])
@jwt_required()
@validate_json(['fatigue', 'stress', 'motivation'])
def submit_mood():
	"""
	Endpoint: POST /api/mood
	Opis: Przesłanie danych samopoczucia i generowanie planu treningowego
	"""
	user_id = get_jwt_identity()
	data = request.get_json()
	fatigue = data.get('fatigue')
	stress = data.get('stress')
	motivation = data.get('motivation')
	# Validacja zakresu
	if not (1 <= fatigue <= 10 and 1 <= stress <= 10 and 1 <= motivation <= 10):
		return jsonify({'error': 'Wartości muszą być w zakresie 1-10'}), 400
	# Zapis do bazy
	mood_log = MoodLog(
		user_id=user_id,
		fatigue=fatigue,
		stress=stress,
		motivation=motivation
	)
	db.session.add(mood_log)
	db.session.commit()
	# Predykcja intensywności
	intensity = ai_service.predict_intensity(user_id, fatigue, stress, motivation)
	# Generowanie planu
	workout_plan = ai_service.generate_workout_plan(intensity)
	# Zapis planu do bazy
	workout = Workout(
		user_id=user_id,
		mood_log_id=mood_log.id,
		workout_type=workout_plan['type'],
		intensity=intensity,
		exercises=workout_plan['exercises']
	)
	db.session.add(workout)
	db.session.commit()
	return jsonify({
		'success': True,
		'mood': mood_log.to_dict(),
		'workout': workout.to_dict(),
		'message': 'Plan treningowy wygenerowany pomyślnie'
	}), 200
@mood_bp.route('/history', methods=['GET'])
@jwt_required()
def get_mood_history():
	"""
	Endpoint: GET /api/mood/history
	Opis: Pobieranie historii samopoczucia użytkownika
	"""
	user_id = get_jwt_identity()
	mood_logs = MoodLog.query.filter_by(user_id=user_id)\
		.order_by(MoodLog.timestamp.desc()).all()
	return jsonify({
		'success': True,
		'data': [log.to_dict() for log in mood_logs]
	}), 200