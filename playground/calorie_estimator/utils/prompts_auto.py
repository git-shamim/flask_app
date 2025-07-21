"""
Auto-generated prompts for food calorie estimation and health evaluation.
"""

def get_calorie_estimation_prompt(food_name: str) -> str:
    """
    Returns a structured prompt for calorie and macronutrient breakdown.
    """
    safe_name = food_name.strip().title()

    return (
        f"Estimate the calories and macronutrient breakdown for a typical serving of '{safe_name}'.\n\n"
        f"Please include:\n"
        f"• Estimated calories (in kcal)\n"
        f"• Carbohydrates (in grams)\n"
        f"• Protein (in grams)\n"
        f"• Fat (in grams)\n"
        f"• Serving size used for estimation\n\n"
        f"Respond in clear, bullet-point format."
    )


def get_health_evaluation_prompt(food_name: str) -> str:
    """
    Returns a concise prompt for health evaluation.
    """
    safe_name = food_name.strip().title()

    return (
        f"Provide a health evaluation of the dish '{safe_name}' in under 100 words.\n"
        f"Include 2–3 key nutritional points and any dietary warnings. "
        f"Be objective, friendly, and informative."
    )
