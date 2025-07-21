import os
from PIL import Image
import torch

USE_BLIP = os.getenv("USE_BLIP", "1") == "1"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Lazy globals
_blip_processor = None
_blip_model = None

def _load_blip_model():
    """
    Load BLIP processor and model only once.
    """
    global _blip_processor, _blip_model
    if _blip_processor is None or _blip_model is None:
        from transformers import BlipProcessor, BlipForConditionalGeneration
        _blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        _blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        _blip_model.to(device)

def generate_caption(pil_image: Image.Image) -> str:
    """
    Generate a caption using BLIP, or return fallback if in minimal mode.
    """
    try:
        if not USE_BLIP:
            return "[BLIP disabled in Cloud Run – skipping caption generation]"

        _load_blip_model()
        inputs = _blip_processor(images=pil_image, return_tensors="pt").to(device)

        with torch.no_grad():
            out = _blip_model.generate(**inputs)

        caption = _blip_processor.decode(out[0], skip_special_tokens=True)
        return caption

    except Exception as e:
        return f"Error generating caption: {e}"
