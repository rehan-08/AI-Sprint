import numpy as np
import pickle
from typing import List, Tuple, Optional
from config import settings
from utils.text_normalizer import normalize_ingredient

# Load models
with open(settings.TFIDF_PATH, 'rb') as f:
    vectorizer = pickle.load(f)
with open(settings.KNN_PATH, 'rb') as f:
    knn = pickle.load(f)
with open(settings.INTERACTION_MAP_PATH, 'rb') as f:
    data = pickle.load(f)
    training_pairs = data['pairs']
    training_severities = data['severities']
    training_descriptions = data['descriptions']
    training_risk_levels = data['risk_levels']
    training_affected_organs = data['affected_organs']
    pair_map = data['pair_map']

def predict_interaction(ing1: str, ing2: str, threshold=0.7) -> Optional[dict]:
    """
    Predict interaction for unknown pair.
    Returns dict with severity, description, risk_level, affected_organ if confident enough.
    """
    norm1 = normalize_ingredient(ing1)
    norm2 = normalize_ingredient(ing2)
    combined = " ".join(sorted([norm1, norm2]))

    # Exact match
    if combined in pair_map:
        result = pair_map[combined].copy()
        result['ai_generated'] = False
        return result

    # kNN prediction
    vec = vectorizer.transform([combined])
    distances, indices = knn.kneighbors(vec)

    similarities = 1 - distances[0]
    valid_indices = [i for i, sim in zip(indices[0], similarities) if sim >= threshold]
    if not valid_indices:
        return None

    # Majority voting for categorical fields
    neighbor_severities = [training_severities[i] for i in valid_indices]
    neighbor_risk_levels = [training_risk_levels[i] for i in valid_indices]
    neighbor_organs = [training_affected_organs[i] for i in valid_indices]

    # Severity priority: Major > Moderate > Minor
    severity_order = {"Major": 3, "Moderate": 2, "Minor": 1}
    predicted_severity = max(neighbor_severities, key=lambda s: severity_order.get(s, 0))

    # Risk level priority: High > Moderate > Mild
    risk_order = {"High": 3, "Moderate": 2, "Mild": 1}
    predicted_risk = max(neighbor_risk_levels, key=lambda r: risk_order.get(r, 0))

    # Most common affected organ
    from collections import Counter
    predicted_organ = Counter(neighbor_organs).most_common(1)[0][0]

    # Combine descriptions
    neighbor_descriptions = set(training_descriptions[i] for i in valid_indices)
    description = "Possible interaction based on similar ingredients: " + "; ".join(neighbor_descriptions)

    return {
        "severity": predicted_severity,
        "description": description,
        "risk_level": predicted_risk,
        "affected_organ": predicted_organ,
        "ai_generated": True
    }