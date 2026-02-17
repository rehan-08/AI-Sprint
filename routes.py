from fastapi import FastAPI, HTTPException
from api.schemas import InteractionRequest, InteractionResponse
from database.db import check_all_interactions
from database.disease_map import get_diseases   # new
from utils.response_generator import generate_warning, should_consult
from database.models import IngredientInteraction

app = FastAPI(title="AI Ingredient Interaction Checker", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Ingredient Interaction API is running. Use POST /check-interactions"}

@app.post("/check-interactions", response_model=InteractionResponse)
def check_interactions(request: InteractionRequest):
    if not request.ingredients or len(request.ingredients) < 2:
        raise HTTPException(status_code=400, detail="At least two ingredients are required.")

    # Gather disease info for each ingredient
    ingredient_details = {}
    for ing in request.ingredients:
        diseases = get_diseases(ing)
        if diseases:
            ingredient_details[ing] = diseases

    interactions = check_all_interactions(request.ingredients)
    ingredient_interactions = [
        IngredientInteraction(
            ingredient1=i["ingredient1"],
            ingredient2=i["ingredient2"],
            severity=i["severity"],
            description=i["description"] + (" (AI predicted)" if i.get("ai_generated") else ""),
            risk_level=i["risk_level"],
            affected_organ=i["affected_organ"],
            ai_generated=i.get("ai_generated", False)
        ) for i in interactions
    ]

    warning = generate_warning(ingredient_interactions)
    consultation = should_consult(ingredient_interactions)

    return InteractionResponse(
        interactions=ingredient_interactions,
        ingredient_details=ingredient_details,
        warning=warning,
        consultation_advised=consultation
    )