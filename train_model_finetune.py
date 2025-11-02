# train_model_finetune.py

import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import json

# ============================
# CONFIGURATION
# ============================
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS_STAGE1 = 10
EPOCHS_STAGE2 = 25
DATASET_DIR = r"D:\N-Developer\my project\skin_app\dataset\train_combined"
MODEL_PATH = r"D:\N-Developer\my project\skin_app\model\skin_model_final_v3.h5"

# ============================
# DATA PREPARATION
# ============================
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    zoom_range=0.25,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    shear_range=0.15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    fill_mode="nearest",
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

num_classes = len(train_data.class_indices)
print(f"\n📊 Found {train_data.samples} training images across {num_classes} classes.")

# ============================
# CLASS WEIGHTS
# ============================
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(train_data.classes),
    y=train_data.classes
)
class_weights = dict(enumerate(class_weights))
print("\n⚖️ Class Weights:", class_weights)

# ============================
# MODEL (MobileNetV2)
# ============================
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)  # ✅ کمک به پایداری
x = Dropout(0.4)(x)
x = Dense(256, activation="relu")(x)
x = Dropout(0.3)(x)
predictions = Dense(num_classes, activation="softmax")(x)
model = Model(inputs=base_model.input, outputs=predictions)

# ============================
# CALLBACKS
# ============================
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

callbacks = [
    EarlyStopping(monitor="val_loss", patience=6, restore_best_weights=True, verbose=1),
    ModelCheckpoint(MODEL_PATH, monitor="val_accuracy", save_best_only=True, verbose=1),
    ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=3, min_lr=1e-6, verbose=1)  # ✅ کاهش داینامیک نرخ یادگیری
]

# ============================
# STAGE 1: TRAIN TOP LAYERS
# ============================
print("\n🔹 Stage 1: Training top layers (base frozen)...")
model.compile(optimizer=Adam(learning_rate=1e-4), loss="categorical_crossentropy", metrics=["accuracy"])

history1 = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_STAGE1,
    class_weight=class_weights,
    callbacks=callbacks
)

# ============================
# STAGE 2: FINE-TUNING
# ============================
print("\n🔹 Stage 2: Fine-tuning deeper layers...")
base_model.trainable = True
for layer in base_model.layers[:-40]:
    layer.trainable = False

model.compile(optimizer=Adam(learning_rate=1e-5), loss="categorical_crossentropy", metrics=["accuracy"])

history2 = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_STAGE2,
    class_weight=class_weights,
    callbacks=callbacks
)

# ============================
# FINAL SAVE
# ============================
model.save(MODEL_PATH)
print(f"\n✅ Model saved at: {MODEL_PATH}")

# ============================
# CLASS MAPPING
# ============================
print("\n🩺 Classes detected:")
for k, v in train_data.class_indices.items():
    print(f"{v}: {k}")

with open(r"D:\N-Developer\my project\skin_app\model\class_indices.json", "w", encoding="utf-8") as f:
    json.dump(train_data.class_indices, f, ensure_ascii=False, indent=2)

print("\n📁 Class index mapping saved successfully!")
