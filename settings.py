import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "drug_interactions.csv")
DISEASE_DATA_PATH = os.path.join(DATA_DIR, "raw", "ingredient_diseases.csv")   # new
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed", "cleaned_drugs.csv")
MODEL_ASSETS_DIR = os.path.join(DATA_DIR, "processed", "model_assets")

os.makedirs(MODEL_ASSETS_DIR, exist_ok=True)

TFIDF_PATH = os.path.join(MODEL_ASSETS_DIR, "tfidf_vectorizer.pkl")
KNN_PATH = os.path.join(MODEL_ASSETS_DIR, "knn_model.pkl")
INTERACTION_MAP_PATH = os.path.join(MODEL_ASSETS_DIR, "interaction_map.pkl")