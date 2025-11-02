import os
import shutil

# =====================
# Dataset paths (your 5 folders)
# =====================
DATASET_PATHS = [
    r"D:\N-Developer\my project\skin_app\model downloaded\7 classes",
    r"D:\N-Developer\my project\skin_app\model downloaded\Skin diseases image dataset (10 classes)",
    r"D:\N-Developer\my project\skin_app\model downloaded\20 Skin Diseases Dataset (300 MB)",
    r"D:\N-Developer\my project\skin_app\model downloaded\23 classes",
    r"D:\N-Developer\my project\skin_app\model downloaded\Skin-Disease (8 classes)",
]

# Target directory for merged dataset
TARGET_DIR = r"D:\N-Developer\my project\skin_app\dataset\train_combined"
os.makedirs(TARGET_DIR, exist_ok=True)

# =====================
# Folder rename map (standardized class names)
# =====================
rename_map = {
    # --- 7-class dataset ---
    "akiec": "actinic_keratosis",
    "bcc": "basal_cell_carcinoma",
    "bkl": "benign_keratosis_lesion",
    "df": "dermatofibroma",
    "mel": "melanoma",
    "nv": "melanocytic_nevi",
    "vasc": "vascular_lesion",

    # --- Common class names found in 10, 20, and 23 class datasets ---
    "Eczema": "eczema",
    "Atopic": "atopic_dermatitis",
    "Basal": "basal_cell_carcinoma",
    "Melanoma": "melanoma",
    "Melanocytic": "melanocytic_nevi",
    "Benign": "benign_keratosis_lesion",
    "Psoriasis": "psoriasis",
    "Seborrheic": "seborrheic_keratosis",
    "Tinea": "tinea_ringworm",
    "Warts": "warts_molluscum",
    "Acne": "acne_rosacea",
    "Rosacea": "acne_rosacea",
    "Bullous": "bullous_disease",
    "Cellulitis": "cellulitis",
    "Drug": "drug_eruptions",
    "Exanthem": "drug_eruptions",
    "Herpes": "herpes_hpv",
    "HPV": "herpes_hpv",
    "Light": "light_disorders",
    "Lupus": "lupus",
    "Poison": "poison_ivy",
    "Systemic": "systemic_disease",
    "Urticaria": "urticaria_hives",
    "Vasculitis": "vasculitis",
    "Vascular Tumors": "vascular_tumors",
    "Viral": "warts_molluscum",
    "Hair Loss": "hair_loss_alopecia",
    "Nail Fungus": "nail_fungus",
    "Scabies": "scabies_lyme_disease",
    "Lyme": "scabies_lyme_disease",

    # --- Skin-Disease (8 classes) ---
    "impetigo": "impetigo",
    "athlete-foot": "athlete_foot",
    "nail-fungus": "nail_fungus",
    "ringworm": "tinea_ringworm",
    "shingles": "shingles",
    "chickenpox": "chickenpox",
    "cutaneous-larva-migrans": "cutaneous_larva_migrans",
}

def match_class(folder_name):
    """Match folder name with standardized class key"""
    for key, val in rename_map.items():
        if key.lower() in folder_name.lower():
            return val
    return None

# =====================
# Merge all datasets
# =====================
for dataset_path in DATASET_PATHS:
    print(f"\n📂 Processing dataset: {dataset_path}")
    for folder in os.listdir(dataset_path):
        src_folder = os.path.join(dataset_path, folder)
        if not os.path.isdir(src_folder):
            continue

        target_name = match_class(folder)
        if not target_name:
            print(f"⚠️ Skipped (no match): {folder}")
            continue

        dest_folder = os.path.join(TARGET_DIR, target_name)
        os.makedirs(dest_folder, exist_ok=True)

        copied = 0
        for file in os.listdir(src_folder):
            src_file = os.path.join(src_folder, file)
            if not os.path.isfile(src_file):
                continue

            dest_file = os.path.join(dest_folder, f"{target_name}_{len(os.listdir(dest_folder))}.jpg")
            try:
                shutil.copy2(src_file, dest_file)
                copied += 1
            except Exception as e:
                pass

        print(f"✅ Copied {copied} images → {target_name}")

print("\n🎯 Merge completed successfully!")
print(f"📁 All merged data saved in: {TARGET_DIR}")
