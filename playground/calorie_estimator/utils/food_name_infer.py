# playground/calorie_estimator/utils/food_name_infer.py

from .genai_client import query_groq
from .caption_generator import generate_caption
import logging

def infer_food_from_caption(pil_image):
    """
    Generates a caption using BLIP and infers a food name via GenAI.
    Returns (food_name, caption).
    """
    try:
        caption = generate_caption(pil_image)
        if "Error" in caption:
            logging.warning("⚠️ Captioning failed; skipping GenAI query.")
            return "unknown", caption

        prompt = (
            f'The following image caption was generated: "{caption}"\n\n'
            "Based on this caption, what is the most likely name of the food item?\n"
            "Return only the food name. If the caption is not related to food, say 'non-food'."
        )

        food_name = query_groq(prompt)
        return food_name.strip(), caption

    except Exception as e:
        logging.error(f"❌ Error in food name inference: {e}")
        return "unknown", "Error generating caption"
