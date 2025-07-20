# model/imagenet_model.py

import numpy as np
from tensorflow.keras.applications import mobilenet_v2
from tensorflow.keras.preprocessing import image

# Load MobileNetV2 model pretrained on ImageNet
mobilenet = mobilenet_v2.MobileNetV2(weights="imagenet")

# Set of food-related keywords to filter predictions
FOOD_KEYWORDS = {
    "pizza", "sandwich", "burger", "hotdog", "burrito", "taco",
    "salad", "soup", "noodles", "spaghetti", "cake", "dessert",
    "meat", "steak", "rice", "bread", "food", "dish", "plate",
    "fries", "coffee", "biryani", "idli", "dosa", "samosa", "paneer",
    "chapati", "tikka", "dal", "saag", "kheer", "halwa", "poha", "ladoo"
}

def classify_with_imagenet(pil_image, top_k=3):
    """
    Run classification using MobileNetV2 on an input PIL image.
    Returns top-k decoded predictions.
    """
    img = pil_image.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = mobilenet_v2.preprocess_input(x)

    preds = mobilenet.predict(x, verbose=0)
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
