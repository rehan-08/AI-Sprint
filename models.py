from pydantic import BaseModel
from typing import List, Optional, Dict

class IngredientInteraction(BaseModel):
    ingredient1: str
    ingredient2: str
    severity: str
    description: str
    risk_level: str
    affected_organ: str
    ai_generated: bool = False

class InteractionRequest(BaseModel):
    ingredients: List[str]

class InteractionResponse(BaseModel):
    interactions: List[IngredientInteraction]
    ingredient_details: Dict[str, List[str]]   # new: ingredient -> list of diseases
    warning: Optional[str] = None
    consultation_advised: bool = False