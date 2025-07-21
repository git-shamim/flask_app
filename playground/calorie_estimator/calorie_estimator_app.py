# calorie_estimator_app.py

import os
import sys
import streamlit as st
from PIL import Image

# Local imports
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
# ✅ Streamlit Setup
# ──────────────────────────────
st.set_page_config(page_title="Food Calorie Estimator", layout="wide")
st.title("🍱 Food Item Detection & Calorie Estimation")
st.markdown("Follow the steps to estimate calories, evaluate healthiness, and improve your food choices.")

# ──────────────────────────────
# ✅ Session Initialization
# ──────────────────────────────
for key in ["confirmed_food_name", "last_uploaded_file"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ──────────────────────────────
# ✅ Step 1: Upload Image
# ──────────────────────────────
uploaded_file = st.file_uploader("📤 Step 1: Upload a food image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    sig = f"{uploaded_file.name}_{uploaded_file.size}"
    if st.session_state.last_uploaded_file != sig:
        st.session_state.last_uploaded_file = sig
        st.session_state.confirmed_food_name = None
        st.session_state.pop("food_name_input", None)  # Clean reset

    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)

    # ── Detect Image Contents ──
    with st.spinner("🔍 Detecting food type..."):
        is_food, label, confidence = is_food_image(image, threshold=0.7)

    if is_food:
        st.success(f"✅ Detected: **{label}** ({confidence:.2%} confidence)")
        default_input = label
    else:
        food_name, caption = infer_food_from_caption(image)
        st.info(f"📝 Caption: *{caption}*")
        st.success(f"🧠 GenAI suggests: **{food_name}**")
        default_input = food_name

    if "food_name_input" not in st.session_state:
        st.session_state["food_name_input"] = default_input

    # ──────────────────────────────
    # ✅ Step 2: Confirm Food Name
    # ──────────────────────────────
    st.markdown("### Step 2: Confirm the food name")
    with st.form("confirm_food"):
        food_name = st.text_input("👉 Enter or edit the food name below:", key="food_name_input")
        if st.form_submit_button("✅ Confirm Food Name") and food_name.strip():
            st.session_state.confirmed_food_name = food_name.strip()

# ──────────────────────────────
# ✅ Step 3: Estimate & Evaluate
# ──────────────────────────────
if st.session_state.confirmed_food_name:
    food_name = st.session_state.confirmed_food_name
    st.markdown(f"### 🍽️ Results for **{food_name}**")

    with st.spinner("🧮 Estimating..."):
        cal_response = query_groq(get_calorie_estimation_prompt(food_name))
        health_response = query_groq(get_health_evaluation_prompt(food_name), max_tokens=250)

    st.subheader("🔥 Calorie Breakdown")
    st.markdown(cal_response)
    st.subheader("❤️ Health Evaluation")
    st.markdown(health_response)

    # ──────────────────────────────
    # ✅ Step 4: Tip
    # ──────────────────────────────
    with st.form("health_tip_form"):
        if st.form_submit_button("💡 Suggest a Simple Health Tip"):
            with st.spinner("✨ Generating tip..."):
                tip_prompt = (
                    f"Suggest a short, practical tip (1–2 sentences) to make '{food_name}' healthier "
                    f"without losing its core taste. Avoid generic advice."
                )
                tip_response = query_groq(tip_prompt, max_tokens=150)

            st.subheader("💡 Health Tip")
            st.markdown(tip_response)
