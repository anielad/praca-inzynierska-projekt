import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import joblib
class ModelTrainer:
	def __init__(self, data_path='training_data.csv'):
		self.data = pd.read_csv(data_path)
		self.model = None

	def prepare_data(self):
		"""Przygotowanie danych treningowych"""
		X = self.data[['fatigue', 'stress', 'motivation', 'avg_volume', 'days_since_last']]
		y = self.data['intensity_score']
		# Normalizacja cech
		X_normalized = X.copy()
		X_normalized = (X_normalized - X_normalized.mean()) / X_normalized.std()
		return X_normalized, y

	def train_model(self):
		"""Trenowanie modelu Random Forest"""
		X, y = self.prepare_data()
		# Podział danych
		X_train, X_test, y_train, y_test = train_test_split(
			X, y, test_size=0.2, random_state=42
		)
		# Trenowanie
		self.model = RandomForestRegressor(
			n_estimators=100,
			max_depth=15,
			min_samples_split=5,
			random_state=42,
			n_jobs=-1
		)
		self.model.fit(X_train, y_train)
		# Ocena
		train_score = self.model.score(X_train, y_train)
		test_score = self.model.score(X_test, y_test)
		y_pred = self.model.predict(X_test)
		rmse = np.sqrt(mean_squared_error(y_test, y_pred))
		print(f"Train R²: {train_score:.4f}")
		print(f"Test R²: {test_score:.4f}")
		print(f"RMSE: {rmse:.4f}")
		return self.model, test_score, rmse

	def save_model(self, path='app/ai/model.pkl'):
		"""Zapis modelu do pliku"""
		if self.model:
			joblib.dump(self.model, path)
			print(f"Model zapisany: {path}")

# Przykład użycia
if __name__ == '__main__':
	trainer = ModelTrainer('training_data.csv')
	model, score, rmse = trainer.train_model()
	trainer.save_model()