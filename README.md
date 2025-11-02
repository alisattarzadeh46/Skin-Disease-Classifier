# 🩺 Skin Disease Classifier | تشخیص خودکار بیماری‌های پوستی

A bilingual (English–Persian) deep learning-based desktop application for **automatic skin disease classification**, built using **TensorFlow**, **Keras**, and **Tkinter GUI**.

این نرم‌افزار به صورت **دو‌زبانه (فارسی و انگلیسی)** طراحی شده و قادر است بیماری‌های پوستی را از روی تصویر کاربر شناسایی کند.  
کاربر می‌تواند ۱ تا ۳ تصویر پوستی را بارگذاری کند تا مدل بیماری را پیش‌بینی و توضیحات و درمان پیشنهادی را نمایش دهد.

---

## 🌍 Languages | زبان‌ها
- English 🇬🇧  
- فارسی 🇮🇷  

The user can switch between English and Persian interfaces using language buttons on the top of the app window.  
کاربر می‌تواند با انتخاب پرچم‌ها، زبان رابط کاربری را تغییر دهد.

---

## 🚀 Features | ویژگی‌ها
- 🔍 Upload and classify **1–3 skin images** instantly  
- 🧠 Fine-tuned **MobileNetV2** model implemented with TensorFlow/Keras  
- 🌐 **Bilingual interface (Persian + English)**  
- 💊 Integrated buttons for:
  - 🧠 **ChatGPT API** connection *(requires your own API key implementation)*  
  - 🛒 **Drug Store API** integration *(for medical product suggestions)*  
- 📊 Detailed prediction panel including:
  - Disease name  
  - Description  
  - Treatment advice  

---

## 🧠 Model Overview
The classifier uses a **fine-tuned MobileNetV2** architecture trained on multiple public Kaggle datasets of dermatology images for efficient and accurate recognition.

> ⚠️ **Note:**  
> The public version of this repository does **not include** the trained model file (`skin_model_final_v3.h5`) or dataset.  
> You can retrain the model using:
> ```bash
> python train_model_finetune.py
> ```

---

## 🧬 Diseases Covered
This project supports classification of multiple skin conditions, including:
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

---

## 🧪 Datasets Used
Trained using public Kaggle datasets:

1. [20 Skin Diseases Dataset – Haroon Alam](https://www.kaggle.com/datasets/haroonalam16/20-skin-diseases-dataset?resource=download)  
2. [Skin Diseases Image Dataset – Ismail Promus](https://www.kaggle.com/datasets/ismailpromus/skin-diseases-image-datase)  
3. [Skin Disease Dataset – Fares Abbas](https://www.kaggle.com/datasets/faresabbasai2022/skin-disease?utm_source=chatgpt.com)

All datasets were preprocessed, resized, and augmented before training to improve generalization and reduce overfitting.

---

## 🧩 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python run_app.py
   ```
3. Upload your skin image(s) and view the disease prediction.

---

## 🎥 Demo | نمای دمو

A short demo video and interface screenshot are included below.

### ▶️ [Watch the demo video](https://github.com/alisattarzadeh46/Skin-Disease-Classifier/blob/main/demo/demo.mp4)

![App Screenshot](demo/app_interface.jpg)

---

## 🧾 License
Released under the **MIT License** — free for educational and research use.

---

## 👨‍💻 Author
Developed by **Ali Sattarzadeh**  
For academic and research purposes in **Machine Learning** and **Computer Vision**.

> ⭐ If you like this project, please star the repository on GitHub!
