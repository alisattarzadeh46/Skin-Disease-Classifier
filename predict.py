# predict.py (نسخه نهایی)
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os
from data.advice_data import advice_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "skin_model_final_v3.h5")
CLASS_MAP_PATH = os.path.join(BASE_DIR, "model", "class_indices.json")

# --- Load model ---
if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded:", MODEL_PATH)
else:
    model = None
    print("⚠️ Warning: Model not found!")

# --- Load class map ---
if os.path.exists(CLASS_MAP_PATH):
    with open(CLASS_MAP_PATH, "r", encoding="utf-8") as f:
        class_indices = json.load(f)
    index_to_label = {v: k for k, v in class_indices.items()}
else:
    index_to_label = {}
    print("⚠️ class_indices.json not found!")

# --- Prediction helper ---
def _predict_single(image_path):
    """Predict single image"""
    img = Image.open(image_path).convert("RGB").resize((224, 224))
    arr = np.expand_dims(np.array(img) / 255.0, axis=0)
    preds = model.predict(arr, verbose=0)
    return preds


def predict_skin_disease(image_paths):
    """
    Predicts disease name and confidence.
    Returns tuple: (fa_name, confidence_percent, en_name, class_key)
    """
    if model is None:
        return "مدل بارگذاری نشده", 0.0, "Model not loaded", "unknown"

    try:
        # ensure list
        if isinstance(image_paths, str):
            image_paths = [image_paths]

        preds_list = [_predict_single(p) for p in image_paths]
        mean_preds = np.mean(preds_list, axis=0)
        idx = int(np.argmax(mean_preds))
        confidence = float(np.max(mean_preds)) * 100
        class_key = index_to_label.get(idx, "unknown").lower().strip()

        # 🔹 نام‌های اختیاری برای کلاس‌های خاص (اختصار)
        LABEL_NAMES = {
            "acne_rosacea": {"en": "Rosacea", "fa": "رزاسه"},
            "actinic_keratosis": {"en": "Actinic Keratosis", "fa": "کراتوز آکتینیک"},
            "psoriasis": {"en": "Psoriasis", "fa": "پسوریازیس"},
            "ringworm": {"en": "Ringworm", "fa": "قارچ پوستی"},
            "tinea_ringworm": {"en": "Ringworm", "fa": "قارچ پوستی"},
        }

        # --- اگر در لیست بالا بود ---
        if class_key in LABEL_NAMES:
            names = LABEL_NAMES[class_key]
            return names["fa"], confidence, names["en"], class_key

        # --- اگر در advice_data بود ---
        if class_key in advice_data:
            fa_name = advice_data[class_key].get("fa", {}).get("name", "نامشخص")
            en_name = advice_data[class_key].get("en", {}).get("name", "Unknown")
            return fa_name, confidence, en_name, class_key

        # --- اگر ناشناخته بود ---
        return "ناشناخته", confidence, "Unknown", class_key

    except Exception as e:
        print("❌ Error during prediction:", e)
        return "خطا در پردازش", 0.0, "Error", "error"
