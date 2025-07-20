from flask import Blueprint, render_template, request, current_app
from PIL import Image
from playground.calorie_estimator.utils.genai_client import query_groq
from playground.calorie_estimator.utils.imagenet_model import is_food_image
from playground.calorie_estimator.utils.caption_generator import generate_caption
from playground.calorie_estimator.utils.food_name_infer import infer_food_from_caption
from playground.calorie_estimator.utils.prompts_auto import (
    get_calorie_estimation_prompt,
    get_health_evaluation_prompt
)

calorie_estimator_bp = Blueprint(
    'calorie_estimator_bp', __name__, template_folder='templates'
)

@calorie_estimator_bp.route("/playground/calorie-estimator", methods=["GET", "POST"])
def calorie_estimator():
    result = {}
    food_name = None
    uploaded_file = None

    if request.method == "POST":
        uploaded_file = request.files.get("image")
        manual_food_name = request.form.get("manual_food_name", "").strip()

        if uploaded_file:
            try:
                image = Image.open(uploaded_file).convert("RGB")

                # Step 1: Detect if it's a food image
                is_food, label, confidence = is_food_image(image, threshold=0.7)

                if is_food:
                    food_name = label
                    result["detection"] = f"✅ Detected as: {label} ({confidence:.2%} confidence)"
                else:
                    # Step 2: Fallback to caption + GenAI
                    inferred_name, caption = infer_food_from_caption(image)
                    food_name = inferred_name
                    result["caption"] = caption
                    result["inferred_food_name"] = inferred_name
                    result["detection"] = f"🧠 GenAI suggests: {inferred_name}"

                # Step 3: Override if user manually edited
                if manual_food_name:
                    food_name = manual_food_name
                    result["manual_override"] = True

                # Step 4: Calorie & Health Evaluation
                result["food_name"] = food_name

                cal_prompt = get_calorie_estimation_prompt(food_name)
                result["calories"] = query_groq(cal_prompt)

                health_prompt = (
                    f"In under 100 words, evaluate whether '{food_name}' is healthy or not. "
                    f"Mention 2–3 nutrition highlights and any dietary precautions."
                )
                result["health_eval"] = query_groq(health_prompt, max_tokens=250)

            except Exception as e:
                current_app.logger.error(f"❌ Error processing image: {e}")
                result["error"] = "Unable to process the uploaded image."

    return render_template(
        "playground/calorie_estimator.html",
        result=result,
        uploaded_filename=uploaded_file.filename if uploaded_file else None
    )
