from typing import List
from database.models import IngredientInteraction

def generate_warning(interactions: List[IngredientInteraction]) -> str:
    if not interactions:
        return "No known interactions found."

    high_risk = any(i.risk_level.lower() == "high" for i in interactions)
    moderate_risk = any(i.risk_level.lower() == "moderate" for i in interactions)

    # Group by affected organ for better warning
    organs = set(i.affected_organ for i in interactions if i.affected_organ)

    if high_risk:
        organ_text = f" affecting {', '.join(organs)}" if organs else ""
        return f"⚠️ DANGEROUS: High-risk interaction(s) detected{organ_text}. Immediate medical consultation recommended."
    elif moderate_risk:
        organ_text = f" affecting {', '.join(organs)}" if organs else ""
        return f"⚠️ Caution: Moderate-risk interaction(s) found{organ_text}. Consult your healthcare provider."
    else:
        return "ℹ️ Mild interactions present. Monitor for any side effects."

def should_consult(interactions: List[IngredientInteraction]) -> bool:
    return any(i.risk_level.lower() in ["high", "moderate"] for i in interactions)