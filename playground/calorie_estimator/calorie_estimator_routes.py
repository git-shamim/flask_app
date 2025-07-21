# playground/calorie_estimator/calorie_estimator_routes.py

from flask import Blueprint, render_template, request, current_app
from PIL import Image

# Utility imports
from playground.calorie_estimator.utils.genai_client import query_groq
from playground.calorie_estimator.utils.imagenet_model import is_food_image
from playground.calorie_estimator.utils.caption_generator import generate_caption
from playground.calorie_estimator.utils.food_name_infer import infer_food_from_caption
from playground.calorie_estimator.utils.prompts_auto import (
    get_calorie_estimation_prompt,
    get_health_evaluation_prompt
)

# ─── Blueprint Registration ────────────────────────────────────────────────
calorie_estimator_bp = Blueprint(
    'calorie_estimator_bp', __name__, template_folder='templates'
)

@calorie_estimator_bp.route("/playground/food-calorie-estimator", methods=["GET", "POST"])
def calorie_estimator():
    result = {}
    food_name = None
    uploaded_file = None

    if request.method == "POST":
        uploaded_file = request.files.get("image")
        manual_food_name = request.form.get("manual_food_name", "").strip()

        current_app.logger.info("📥 Received POST to calorie estimator")

        if not uploaded_file:
            result["error"] = "No image uploaded."
            return render_template("playground/calorie_estimator.html", result=result)

        try:
            image = Image.open(uploaded_file).convert("RGB")

            # Step 1: Try to classify using pretrained model
            is_food, label, confidence = is_food_image(image, threshold=0.7)

            if is_food:
                food_name = label
                result["detection"] = f"✅ Detected as: {label} ({confidence:.2%} confidence)"
            else:
                # Step 2: Use fallback caption + GenAI-based food inference
                inferred_name, caption = infer_food_from_caption(image)
                food_name = inferred_name
                result.update({
                    "caption": caption,
                    "inferred_food_name": inferred_name,
                    "detection": f"🧠 GenAI suggests: {inferred_name}"
                })

            # Step 3: User manual override
            if manual_food_name:
                food_name = manual_food_name
                result["manual_override"] = True

            result["food_name"] = food_name

            # Step 4: Query Groq for calorie and health evaluation
            if food_name:
                calorie_prompt = get_calorie_estimation_prompt(food_name)
                result["calories"] = query_groq(calorie_prompt)

                health_prompt = get_health_evaluation_prompt(food_name)
                result["health_eval"] = query_groq(health_prompt, max_tokens=250)
            else:
                result["error"] = "Could not determine the food item."

        except Exception as e:
            current_app.logger.error(f"❌ Image processing error: {e}")
            result["error"] = "Unable to process the uploaded image."

    return render_template(
        "playground/calorie_estimator.html",
        result=result,
        uploaded_filename=uploaded_file.filename if uploaded_file else None
    )
