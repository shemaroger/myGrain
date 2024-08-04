from django.apps import AppConfig
import joblib
import os

class GrainHarverstAppConfig(AppConfig):
    name = 'grain_harverst_app'
    maize_model = None
    rice_model = None

    def ready(self):
        maize_model_path = os.path.join(os.path.dirname(__file__), 'maize_quality_models.pkl')
        rice_model_path = os.path.join(os.path.dirname(__file__), 'rice_quality_model.pkl')

        if os.path.exists(maize_model_path):
            self.maize_model = joblib.load(maize_model_path)
            print(f"Maize model loaded from {maize_model_path}")
        else:
            print(f"Maize model file not found at {maize_model_path}")

        if os.path.exists(rice_model_path):
            self.rice_model = joblib.load(rice_model_path)
            print(f"Rice model loaded from {rice_model_path}")
        else:
            print(f"Rice model file not found at {rice_model_path}")
