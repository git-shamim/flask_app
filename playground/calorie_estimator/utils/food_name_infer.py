from .genai_client import query_groq
from .caption_generator import generate_caption

def infer_food_from_caption(pil_image):
    """
    Generates a caption using BLIP and infers a food name via GenAI.
    Returns (food_name, caption).
    """
    caption = generate_caption(pil_image)

    prompt = f"""The following image caption was generated: "{caption}"

    Based on this caption, what is the most likely name of the food item?
    Return only the food name. If the caption is not related to food, say "non-food".
    """

    food_name = query_groq(prompt)
    return food_name.strip(), caption
