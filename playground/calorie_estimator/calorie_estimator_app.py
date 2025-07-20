import os
import sys
import streamlit as st
from PIL import Image
from playground.calorie_estimator.utils.genai_client import query_groq
from playground.calorie_estimator.utils.imagenet_model import is_food_image
from playground.calorie_estimator.utils.caption_generator import generate_caption
from playground.calorie_estimator.utils.food_name_infer import infer_food_from_caption
from playground.calorie_estimator.utils.prompts_auto import (
    get_calorie_estimation_prompt,
    get_health_evaluation_prompt
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# ──────────────────────────────
# ✅ PAGE SETUP
# ──────────────────────────────
st.set_page_config(page_title="Food Calorie Estimator", layout="wide")
st.title("🍱 Food Item Detection & Calorie Estimation")
st.markdown("Follow the steps to estimate calories, evaluate healthiness, and improve your food choices.")

# ──────────────────────────────
# ✅ SESSION STATE INIT
# ──────────────────────────────
if "confirmed_food_name" not in st.session_state:
    st.session_state.confirmed_food_name = None
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None

# ──────────────────────────────
# ✅ IMAGE UPLOAD
# ──────────────────────────────
uploaded_file = st.file_uploader("📤 Step 1: Upload a food image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Detect new upload
    file_signature = f"{uploaded_file.name}_{uploaded_file.size}"
    if st.session_state.last_uploaded_file != file_signature:
        st.session_state.last_uploaded_file = file_signature
        st.session_state.confirmed_food_name = None
        if "food_name_input" in st.session_state:
            del st.session_state["food_name_input"]  # ← Proper reset without warning

    image = Image.open(uploaded_file).convert("RGB")
    st.markdown("### Preview")
    st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)

    # ──────────────────────────────
    # ✅ MODEL INFERENCE
    # ──────────────────────────────
    with st.spinner("🔍 Detecting food type..."):
        is_food, label, confidence = is_food_image(image, threshold=0.7)

    default_input = ""
    if not is_food:
        # Fall back to caption generation + GenAI
        food_name, caption = infer_food_from_caption(image)
        st.info(f"📝 Caption: *{caption}*")
        st.success(f"🧠 GenAI suggests: **{food_name}**")
        default_input = food_name
    else:
        st.success(f"✅ Detected: **{label}** (confidence: {confidence:.2%})")
        default_input = label

    # Set default input only if not already present
    if "food_name_input" not in st.session_state:
        st.session_state["food_name_input"] = default_input

    # ──────────────────────────────
    # ✅ STEP 2: CONFIRM FOOD NAME
    # ──────────────────────────────
    st.markdown("### Step 2: Confirm the food name")
    with st.form("confirm_food"):
        food_name = st.text_input("👉 Enter or edit the food name below:", key="food_name_input")
        confirm = st.form_submit_button("✅ Confirm Food Name")

    if confirm and food_name.strip():
        st.session_state.confirmed_food_name = food_name.strip()

# ──────────────────────────────
# ✅ STEP 3: ESTIMATE & EVALUATE
# ──────────────────────────────
if st.session_state.confirmed_food_name:
    food_name = st.session_state.confirmed_food_name
    st.markdown(f"### 🍽️ Results for **{food_name}**")

    with st.spinner("Estimating calories and evaluating health..."):
        cal_prompt = get_calorie_estimation_prompt(food_name)
        cal_response = query_groq(cal_prompt)

        health_prompt = (
            f"In under 100 words, evaluate whether '{food_name}' is healthy or not. "
            f"Mention 2–3 nutrition highlights and any dietary precautions."
        )
        health_response = query_groq(health_prompt, max_tokens=250)

    # Show outputs in sequence (not columns)
    st.subheader("🔥 Calorie Breakdown")
    st.markdown(cal_response)

    st.subheader("❤️ Health Evaluation")
    st.markdown(health_response)

    # ──────────────────────────────
    # ✅ STEP 4: HEALTH TIP
    # ──────────────────────────────
    st.markdown("### 🌱 Step 4: Improve Your Meal")
    with st.form("health_tip_form"):
        tip_button = st.form_submit_button("💡 Suggest a Simple Health Tip")

    if tip_button:
        with st.spinner("Generating tip..."):
            tip_prompt = (
                f"Suggest a short, practical tip (1–2 sentences) to make '{food_name}' healthier "
                f"without losing its core taste. Avoid generic advice."
            )
            tip_response = query_groq(tip_prompt, max_tokens=150)

        st.subheader("💡 Health Tip")
        st.markdown(tip_response)
