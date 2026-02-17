import pandas as pd
from typing import List, Dict
from config import settings
from utils.text_normalizer import normalize_ingredient

# Global disease map: normalized ingredient -> list of diseases
_disease_map: Dict[str, List[str]] = {}

def load_diseases():
    """Load ingredient-disease mappings from CSV."""
    global _disease_map
    df = pd.read_csv(settings.DISEASE_DATA_PATH)
    for _, row in df.iterrows():
        ing = normalize_ingredient(row["ingredient"])
        disease = row["disease"].strip()
        if ing not in _disease_map:
            _disease_map[ing] = []
        _disease_map[ing].append(disease)

def get_diseases(ingredient: str) -> List[str]:
    """Return list of diseases for a normalized ingredient."""
    norm = normalize_ingredient(ingredient)
    return _disease_map.get(norm, [])

# Load on import
load_diseases()