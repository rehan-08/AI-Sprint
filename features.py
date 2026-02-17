import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from config import settings
from utils.text_normalizer import normalize_ingredient

def prepare_training_data(df: pd.DataFrame):
    df.columns = df.columns.str.strip()  # optional
    pairs = []
    severities = []
    descriptions = []
    risk_levels = []
    affected_organs = []
    pair_to_metadata = {}

    for idx, row in df.iterrows():
        ing1_val = row.get("ingredient1")
        ing2_val = row.get("ingredient2")
        if pd.isna(ing1_val) or pd.isna(ing2_val):
            print(f"Warning: Skipping row {idx} due to missing ingredient")
            continue
        
        ing1 = normalize_ingredient(ing1_val)
        ing2 = normalize_ingredient(ing2_val)
        if not ing1 or not ing2:
            continue  # skip if empty after normalization

        sorted_pair = tuple(sorted([ing1, ing2]))
        combined = " ".join(sorted_pair)

        pairs.append(combined)
        severities.append(row["severity"])
        descriptions.append(row["description"])
        risk_levels.append(row["risk_level"])
        affected_organs.append(row["affected_organ"])
        pair_to_metadata[combined] = {
            "severity": row["severity"],
            "description": row["description"],
            "risk_level": row["risk_level"],
            "affected_organ": row["affected_organ"]
        }

    return pairs, severities, descriptions, risk_levels, affected_organs, pair_to_metadata

def train_tfidf(pairs, max_features=500):
    vectorizer = TfidfVectorizer(max_features=max_features)
    X = vectorizer.fit_transform(pairs)
    return vectorizer, X