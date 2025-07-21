# model/food_detect.py

from .imagenet_model import is_food_image

def detect_food_label_with_fallback(image, threshold: float = 0.70):
    """
    Detects food from image using ImageNet (MobileNetV2) with fallback.

    Args:
        image (PIL.Image): The input image to classify.
        threshold (float): Confidence threshold to validate detection.

    Returns:
        Tuple[str, float, str]: (food_label or 'non-food', confidence, method_used)
    """
    try:
        is_food, label, confidence = is_food_image(image, threshold=threshold)

        if is_food:
            return label, confidence, "mobilenet"

        return "non-food", confidence, "manual"

    except Exception as e:
        # In case the image is corrupt or the model fails
        return "non-food", 0.0, f"error: {str(e)}"
