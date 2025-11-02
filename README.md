# 🩺 Skin Disease Classifier

A bilingual deep learning-based desktop application for **automatic skin disease classification**, built using **TensorFlow**, **Keras**, and **Tkinter GUI**.

This software is capable of identifying skin diseases from user-submitted images.  
Users can upload 1–3 skin images, and the model will predict the disease class, provide a short description, and offer treatment advice.

---

## 🌍 Languages
- English 🇬🇧  
- Persian 🇮🇷  

The application provides a bilingual interface, allowing users to switch between **English** and **Persian** using language buttons located on the top bar.

---

## 🚀 Features
- Upload and classify **1–3 skin images** instantly  
- Fine-tuned **MobileNetV2** model using TensorFlow and Keras  
- **Bilingual user interface** (English + Persian)  
- Integrated buttons for future extensions:  
  - 🧠 **ChatGPT API connection** *(requires your own API key implementation)*  
  - 🛒 **Drug Store API connection** *(for integrating medicine store features)*  
- Displays:
  - Disease name  
  - Description  
  - Treatment advice  

---

## 🧠 Model Overview
The classifier uses a **fine-tuned MobileNetV2** architecture trained on a large dermatology dataset containing **56,000 images** across **30 skin disease categories**.  
It achieves efficient and accurate classification performance suitable for real-time inference on both CPU and GPU.

> ⚠️ **Note:**  
> The public version of this repository does **not include** the trained model file (`skin_model_final_v3.h5`) or datasets.  
> You can retrain your own model using:
> ```bash
> python train_model_finetune.py
> ```

---

## 🧬 Diseases Covered
The model can recognize more than **30 skin disease categories**, including:
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
The model was trained using publicly available Kaggle datasets of dermatological images labeled by experts:

1. [20 Skin Diseases Dataset – Haroon Alam](https://www.kaggle.com/datasets/haroonalam16/20-skin-diseases-dataset?resource=download)  
2. [Skin Diseases Image Dataset – Ismail Promus](https://www.kaggle.com/datasets/ismailpromus/skin-diseases-image-datase)  
3. [Skin Disease Dataset – Fares Abbas](https://www.kaggle.com/datasets/faresabbasai2022/skin-disease?utm_source=chatgpt.com)

After preprocessing, cleaning, and augmentation, the combined dataset contained approximately **56,000 images** of **30 distinct skin conditions**.

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
3. Upload your skin image(s) and view real-time disease predictions.

---

## 🎥 Demo

Below is the demo video and screenshot of the application's interface.

### ▶️ Demo Video
<video src="https://github.com/alisattarzadeh46/Skin-Disease-Classifier/raw/main/demo/demo.mp4" width="700" controls></video>

### 🖼️ App Screenshot
<img src="https://github.com/alisattarzadeh46/Skin-Disease-Classifier/raw/main/demo/Screenshot.jpg" width="600" alt="App Interface">

---

## 🧾 License
Released under the **MIT License** — free for educational, academic, and research use.

---

## 👨‍💻 Author
Developed by **Ali Sattarzadeh**  
For academic and research purposes in **Machine Learning** and **Computer Vision**.

> ⭐ If you like this project, please star the repository on GitHub!
