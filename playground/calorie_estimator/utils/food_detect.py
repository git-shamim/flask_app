# model/food_detect.py

from .imagenet_model import is_food_image

def detect_food_label_with_fallback(image, threshold=0.70):
    """
    Classifies the image using ImageNet (MobileNetV2).
    If confidence >= threshold and food is detected, returns the label.
    Otherwise, returns 'non-food' and prompts the user for manual input.
    """
    is_food, label, confidence = is_food_image(image, threshold=threshold)

    if is_food and confidence >= threshold:
        return label, confidence, "mobilenet"

    return "non-food", confidence, "manual"
