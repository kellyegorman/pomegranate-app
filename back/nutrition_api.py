"""
Nutrition API endpoints for symptom logging and personalized recommendations
"""
from flask import Blueprint, request, jsonify
from back.nutrition_engine import SymptomNutritionEngine, INGREDIENT_BENEFITS

nutrition_bp = Blueprint('nutrition', __name__, url_prefix='/api/nutrition')

# Initialize the nutrition engine
engine = SymptomNutritionEngine()


@nutrition_bp.route('/symptoms', methods=['GET', 'POST'])
def get_symptoms():
    """Get list of available symptoms to log based on life phase"""
    life_phase = None
    if request.method == 'POST' and request.json:
        life_phase = request.json.get('life_phase')
    
    symptoms = engine.get_symptoms(life_phase)
    return {
        "status": "success",
        "symptoms": symptoms,
        "life_phase": life_phase,
        "message": "Available symptoms for logging"
    }


@nutrition_bp.route('/log', methods=['POST'])
def log_symptom():
    """Log a single symptom and get immediate recommendations"""
    data = request.json
    symptom = data.get('symptom')
    
    if not symptom:
        return {"status": "error", "message": "Symptom is required"}, 400
    
    recommendation = engine.log_symptom(symptom)
    
    if not recommendation:
        return {
            "status": "error",
            "message": f"Symptom '{symptom}' not found. Available symptoms: {engine.get_symptoms()}"
        }, 404
    
    return {
        "status": "success",
        "data": recommendation
    }


@nutrition_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get personalized nutrition recommendations based on symptoms and phase"""
    data = request.json
    symptoms_list = data.get('symptoms', [])
    cycle_phase = data.get('cycle_phase')
    life_phase = data.get('life_phase')
    
    if not symptoms_list:
        return {"status": "error", "message": "At least one symptom is required"}, 400
    
    recommendations = engine.get_recommendations(symptoms_list, cycle_phase, life_phase)
    
    # Add ingredient benefits to each recipe
    for recipe in recommendations.get('recipes', []):
        recipe['ingredients_with_benefits'] = [
            {
                'name': ing,
                'benefit': INGREDIENT_BENEFITS.get(ing.lower(), 'Nutrient-rich ingredient supporting your wellness')
            }
            for ing in recipe['ingredients']
        ]
    
    return {
        "status": "success",
        "data": recommendations
    }


@nutrition_bp.route('/quick-snacks', methods=['POST'])
def get_quick_snacks():
    """Get quick 5-minute snack ideas for logged symptoms"""
    data = request.json
    symptoms_list = data.get('symptoms', [])
    
    if not symptoms_list:
        return {"status": "error", "message": "At least one symptom is required"}, 400
    
    snacks = engine.get_quick_snacks(symptoms_list)
    
    return {
        "status": "success",
        "data": snacks,
        "message": f"Found {len(snacks)} quick snack ideas"
    }
