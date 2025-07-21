# model/imagenet_model.py

import numpy as np
from tensorflow.keras.applications import mobilenet_v2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import logging

# Food-related keywords (extended with Indian foods too)
FOOD_KEYWORDS = {
    "pizza", "sandwich", "burger", "hotdog", "burrito", "taco",
    "salad", "soup", "noodles", "spaghetti", "cake", "dessert",
    "meat", "steak", "rice", "bread", "food", "dish", "plate",
    "fries", "coffee", "biryani", "idli", "dosa", "samosa", "paneer",
    "chapati", "tikka", "dal", "saag", "kheer", "halwa", "poha", "ladoo"
}

# Lazy loader for the model
_mobilenet_model = None

def get_mobilenet_model():
    global _mobilenet_model
    if _mobilenet_model is None:
        logging.info("🔄 Loading MobileNetV2 model with ImageNet weights...")
        _mobilenet_model = mobilenet_v2.MobileNetV2(weights="imagenet")
    return _mobilenet_model

def classify_with_imagenet(pil_image, top_k=3):
    """
    Run classification using MobileNetV2 on an input PIL image.
    Returns top-k decoded predictions.
    """
    img = pil_image.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = mobilenet_v2.preprocess_input(x)

    model = get_mobilenet_model()
    preds = model.predict(x, verbose=0)
    decoded = mobilenet_v2.decode_predictions(preds, top=top_k)[0]
    return decoded

def is_food_image(pil_image, threshold=0.7, top_k=3):
    """
    Determine if the image contains food based on top-k predictions.
    Returns: (is_food: bool, label: str, confidence: float)
    """
    predictions = classify_with_imagenet(pil_image, top_k=top_k)
    for _, label, prob in predictions:
        if any(keyword in label.lower() for keyword in FOOD_KEYWORDS) and prob >= threshold:
            return True, label, prob
    return False, predictions[0][1], predictions[0][2]
