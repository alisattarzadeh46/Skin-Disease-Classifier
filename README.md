# 🩺 Skin Disease Classifier

A bilingual deep learning-based desktop application for **automatic skin disease classification**, built using **TensorFlow**, **Keras**, and **Tkinter GUI**.

This software identifies skin diseases from user-submitted images.  
Users can upload 1–3 skin images, and the model will predict the disease type, provide a brief description, and suggest possible treatments.

---

## 🌍 Languages
- English 🇬🇧  
- Persian 🇮🇷  

The application supports a bilingual interface, allowing users to switch between **English** and **Persian** via language buttons on the top bar.

---

## 🚀 Features
- Upload and classify **1–3 skin images** instantly  
- Fine-tuned **MobileNetV2** model using TensorFlow and Keras  
- **Bilingual GUI** (English + Persian)  
- Integrated buttons for:
  - 🧠 **ChatGPT API connection** *(requires your own API key implementation)*  
  - 🛒 **Drug Store API connection** *(for medical product suggestions)*  
- Displays:
  - Disease name  
  - Description  
  - Treatment advice  

---

## 🧠 Model Overview
The classifier uses a **fine-tuned MobileNetV2** trained on **56,000 images** across **30 skin disease classes**.  
It provides high accuracy and runs efficiently on both CPU and GPU.

> ⚠️ **Note:**  
> The public version does **not include** the trained model (`skin_model_final_v3.h5`) or dataset due to size and license restrictions.  
> You can train your own model using:
> ```bash
> python train_model_finetune.py
> ```

---

## 🧪 Datasets Used
Training data was collected from publicly available Kaggle datasets:

1. [20 Skin Diseases Dataset – Haroon Alam](https://www.kaggle.com/datasets/haroonalam16/20-skin-diseases-dataset?resource=download)  
2. [Skin Diseases Image Dataset – Ismail Promus](https://www.kaggle.com/datasets/ismailpromus/skin-diseases-image-datase)  
3. [Skin Disease Dataset – Fares Abbas](https://www.kaggle.com/datasets/faresabbasai2022/skin-disease?utm_source=chatgpt.com)

After preprocessing and augmentation, the final merged dataset contained approximately **56,000 images** across **30 unique classes**.

---

## 🧩 Dataset Preparation and Merging

After downloading the datasets from Kaggle, you must merge them into a single dataset before training.  
Use the provided Python script:

```bash
python merge_skin_datasets.py
```

This script automatically combines all datasets into one unified folder structure suitable for training.  
However, you must **manually update the file and folder paths** inside the script to match your own system directories —  
for example:

```python
# Example inside merge_skin_datasets.py
source_paths = [
    "D:/Datasets/SkinData1/",
    "D:/Datasets/SkinData2/",
    "D:/Datasets/SkinData3/"
]

destination_path = "D:/SkinDiseaseClassifier/data/merged_dataset/"
```

Once merging is complete, proceed to fine-tune the model by running:

```bash
python train_model_finetune.py
```

---

## 🧬 Diseases Covered
This model recognizes a wide range of dermatological conditions, including:
- Acne  
- Eczema  
- Psoriasis  
- Melanoma  
- Basal Cell Carcinoma (BCC)  
- Seborrheic Keratosis  
- Actinic Keratosis  
- Tinea (Ringworm)  
- Rosacea  
- Vitiligo  
...and more (over **30 classes** total).

---

## 🎥 Demo

Below is the demonstration of the **Skin Disease Classifier** application.

### 🖼 App Interface
![App Screenshot](demo/screenshot.jpg)

### 🎬 Live Demo
[Click here to watch the demo video](demo/demo.mp4)

> The demo shows how the user uploads skin images, receives disease predictions, and views bilingual treatment advice.

---

## 🧾 License
Released under the **MIT License** — free for educational, academic, and research use.

---

## 👨‍💻 Author
Developed by **Ali Sattarzadeh**  
For academic and research purposes in **Machine Learning** and **Computer Vision**.

> ⭐ If you like this project, please star the repository on GitHub!
