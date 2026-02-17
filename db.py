import pandas as pd
from typing import List, Dict, Tuple, Optional
from config import settings
from utils.text_normalizer import normalize_ingredient
from ml.predict import predict_interaction

_exact_map: Dict[Tuple[str, str], dict] = {}

def load_exact_interactions():
    global _exact_map
    df = pd.read_csv(settings.RAW_DATA_PATH)
    for _, row in df.iterrows():
        ing1 = normalize_ingredient(row["ingredient1"])
        ing2 = normalize_ingredient(row["ingredient2"])
        key = tuple(sorted([ing1, ing2]))
        _exact_map[key] = {
            "severity": row["severity"],
            "description": row["description"],
            "risk_level": row["risk_level"],
            "affected_organ": row["affected_organ"]
        }

def check_interaction(ing_a: str, ing_b: str) -> Optional[dict]:
    norm_a = normalize_ingredient(ing_a)
    norm_b = normalize_ingredient(ing_b)
    if not norm_a or not norm_b:
        return None

    key = tuple(sorted([norm_a, norm_b]))
    if key in _exact_map:
        result = _exact_map[key].copy()
        result['ai_generated'] = False
        return result

    return predict_interaction(norm_a, norm_b)

def check_all_interactions(ingredients: List[str]) -> List[dict]:
    interactions = []
    n = len(ingredients)
    for i in range(n):
        for j in range(i+1, n):
            result = check_interaction(ingredients[i], ingredients[j])
            if result:
                interactions.append({
                    "ingredient1": ingredients[i],
                    "ingredient2": ingredients[j],
                    "severity": result["severity"],
                    "description": result["description"],
                    "risk_level": result["risk_level"],
                    "affected_organ": result["affected_organ"],
                    "ai_generated": result.get("ai_generated", False)
                })
    return interactions

load_exact_interactions()