def get_calorie_estimation_prompt(food_name: str) -> str:
    return (
        f"Estimate the calories and macronutrient breakdown for a typical serving of '{food_name}'.\n"
        f"Return the following:\n\n"
        f"1. Estimated calories (in kcal)\n"
        f"2. Carbohydrates (in grams)\n"
        f"3. Protein (in grams)\n"
        f"4. Fat (in grams)\n"
        f"5. Serving size used for estimation\n\n"
        f"Format the response in a readable bullet-point format."
    )


def get_health_evaluation_prompt(food_name: str) -> str:
    return (
        f"Provide a health evaluation of the dish '{food_name}' in under 100 words.\n"
        f"Include 2–3 key nutritional aspects and any dietary precautions. "
        f"Be objective and use a friendly tone."
    )
