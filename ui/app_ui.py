# ui/app_ui.py
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
from predict import predict_skin_disease
from data.advice_data import advice_data

# --- Window setup ---
root = tk.Tk()
root.title("Skin Disease Detector | تشخیص بیماری پوستی")
root.geometry("480x900")
root.resizable(False, False)  # ❌ فقط ماکسیمایز ممکن، resize با موس غیرفعال

sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
W, H = 480, 880
root.geometry(f"{W}x{H}+{int((sw-W)/2)}+{int((sh-H)/2)}")

# --- Globals ---
language = "en"
last_prediction = None
selected_images = []   # 1–3 images allowed

# --- Translations ---
translations = {
    "title": {"en": "Skin Disease Detector", "fa": "تشخیص بیماری پوستی"},
    "upload": {"en": "Upload 1–3 Images", "fa": "آپلود ۱ تا ۳ تصویر"},
    "prediction": {"en": "Prediction", "fa": "تشخیص"},
    "confidence": {"en": "Confidence", "fa": "درصد اطمینان"},
    "disease_info": {"en": "About the Disease", "fa": "درباره بیماری"},
    "advice": {"en": "Advice & Treatment", "fa": "توصیه و درمان"},
    "loading": {"en": "Analyzing images...", "fa": "در حال پردازش تصاویر..."},
    "btn_shop": {"en": "💊 Drug Suggestion", "fa": "پیشنهاد دارو 💊"},
    "btn_chat": {"en": "🤖 Doctor Chat", "fa": "چت با پزشک 🤖"},
}

def translate(k):
    return translations[k][language]

# ---------------- language switch ----------------
def switch_language(lang):
    global language
    language = lang
    title_label.config(text=translate("title"))
    upload_button.config(text=translate("upload"))
    prediction_title.config(text=translate("prediction"))
    info_title.config(text=translate("disease_info"))
    advice_title.config(text=translate("advice"))
    btn1.config(text=translate("btn_shop"))
    btn2.config(text=translate("btn_chat"))
    if last_prediction:
        update_ui_with_result(last_prediction)
    show_disease_info(last_prediction[3] if last_prediction else "")
    show_advice(last_prediction[3] if last_prediction else "")

# ---------------- loading ----------------
def show_loading():
    result_label.config(text=translate("loading"), fg="blue", justify="center")
    for t in [info_text, advice_text]:
        t.config(state="normal")
        t.delete(1.0, tk.END)
        t.insert(tk.END, translate("loading"))
        t.config(state="disabled")

# ---------------- upload (1–3 images) ----------------
def upload_images():
    global selected_images
    files = filedialog.askopenfilenames(
        title="Select up to 3 skin images",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if not files:
        return

    selected_images = files[:3]
    show_loading()

    # preview first image
    img = Image.open(selected_images[0]).resize((260, 260))
    tk_img = ImageTk.PhotoImage(img)
    image_label.config(image=tk_img)
    image_label.image = tk_img

    def run_predict():
        result = predict_skin_disease(selected_images)
        root.after(400, lambda: update_ui_with_result(result))

    threading.Thread(target=run_predict, daemon=True).start()

# ---------------- update UI after prediction ----------------
def update_ui_with_result(result):
    """result = (fa_name, confidence, en_name, class_key)"""
    global last_prediction
    fa_name, confidence, en_name, class_key = result
    last_prediction = result

    # ---------------- فارسی ----------------
    if language == "fa":
        name = fa_name.strip()
        conf_text = f"{translate('confidence')} {int(confidence)} درصد"
        display_text = f"{name}\n{conf_text}"

        display_text = "\u202B" + display_text + "\u202C"  # برای راست‌چین کامل

        result_label.config(
            text=display_text,
            fg="green",
            justify="right",
            anchor="e",
            wraplength=360,
            font=("Arial", 13, "bold"),
            bg="white"
        )
        result_label.place(relx=0.98, rely=0.5, anchor="e")

    # ---------------- انگلیسی ----------------
    else:
        name = en_name.strip()
        conf_text = f"{translate('confidence')} {confidence:.1f}%"
        display_text = f"{name}\n{conf_text}"

        result_label.config(
            text=display_text,
            fg="green",
            justify="left",
            anchor="w",
            wraplength=360,
            font=("Arial", 13, "bold"),
            bg="white"
        )
        result_label.place(relx=0.02, rely=0.5, anchor="w")

    # توضیحات جداگانه در فیلدهای مخصوص خودشون نمایش داده می‌شن
    show_disease_info(class_key)
    show_advice(class_key)

# ---------------- info ----------------
def show_disease_info(cls_key):
    info_text.config(state="normal")
    info_text.delete(1.0, tk.END)

    data = advice_data.get(cls_key, {}).get(language, {}).get(
        "what",
        "❌ اطلاعاتی یافت نشد." if language == "fa" else "❌ No info found."
    )

    if language == "fa":
        data = fix_persian_punctuation(data)
        data = make_text_rtl_safe(data)

    info_text.insert(tk.END, data)
    info_text.config(state="disabled")

    if language == "fa":
        info_text.tag_configure("rtl", justify="right", lmargin1=20, lmargin2=20)
        info_text.tag_add("rtl", "1.0", "end")
    else:
        info_text.tag_configure("ltr", justify="left")
        info_text.tag_add("ltr", "1.0", "end")

# ---------------- advice ----------------
def show_advice(cls_key):
    advice_text.config(state="normal")
    advice_text.delete(1.0, tk.END)

    data = advice_data.get(cls_key, {}).get(language, {}).get(
        "treatment",
        "❌ توصیه‌ای یافت نشد." if language == "fa" else "❌ No advice found."
    )

    if language == "fa":
        data = fix_persian_punctuation(data)
        data = make_text_rtl_safe(data)

    advice_text.insert(tk.END, data)
    advice_text.config(state="disabled")

    if language == "fa":
        advice_text.tag_configure("rtl", justify="right", lmargin1=20, lmargin2=20)
        advice_text.tag_add("rtl", "1.0", "end")
    else:
        advice_text.tag_configure("ltr", justify="left")
        advice_text.tag_add("ltr", "1.0", "end")

# ✅ تابع اصلاح نقطه و ویرگول در فارسی
def fix_persian_punctuation(text):
    persian_dot = "۔"   # نقطه فارسی
    persian_comma = "،" # ویرگول فارسی
    fixed = (
        text.replace(".", persian_dot)
            .replace(",", persian_comma)
            .replace(" .", persian_dot)
            .replace(" ,", persian_comma)
    )
    return fixed.strip()

# ✅ تابع اصلاح جهت راست‌به‌چپ برای متن‌های فارسی
def make_text_rtl_safe(text):
    """
    برای متن‌های فارسی که شامل کلمات انگلیسی یا عدد هستند،
    از کاراکترهای جهت‌دهی یونیکد استفاده می‌کند تا نمایش راست‌چین واقعی شود.
    """
    rtl_start = "\u202B"  # Right-to-Left Embedding
    rtl_end = "\u202C"    # Pop Directional Formatting
    return f"{rtl_start}{text}{rtl_end}"


# ======================================================
# ============= UI LAYOUT ==============================
# ======================================================

lang_frame = tk.Frame(root, bg="#f2f2f2")
lang_frame.place(x=10, y=10)

en_flag = ImageTk.PhotoImage(Image.open("assets/flag_uk.png").resize((30, 20)))
fa_flag = ImageTk.PhotoImage(Image.open("assets/flag_ir.png").resize((30, 20)))
tk.Button(lang_frame, image=en_flag, command=lambda: switch_language("en"),
          borderwidth=0, bg="#f2f2f2").grid(row=0, column=0, padx=5)
tk.Button(lang_frame, image=fa_flag, command=lambda: switch_language("fa"),
          borderwidth=0, bg="#f2f2f2").grid(row=0, column=1, padx=5)

title_label = tk.Label(root, text=translate("title"),
                       font=("Arial", 20, "bold"), bg="#f2f2f2")
title_label.place(relx=0.5, y=45, anchor="center")

OFFSET = 30
EXTRA = 5  # 👈 فاصله اضافه بعد از کادر تشخیص

# image
img_frame = tk.Frame(root, width=300, height=260, bg="#d9d9d9")
img_frame.place(x=90, y=50 + OFFSET)
image_label = tk.Label(img_frame, bg="#d9d9d9")
image_label.place(relx=0.5, rely=0.5, anchor="center")

# upload
upload_button = tk.Button(
    root,
    text=translate("upload"),
    command=upload_images,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20,
    height=1
)
upload_button.place(relx=0.5, y=340 + OFFSET, anchor="center")

# prediction
prediction_title = tk.Label(
    root,
    text=translate("prediction"),
    font=("Arial", 15, "bold"),
    bg="#f2f2f2"
)
prediction_title.place(relx=0.5, y=390 + OFFSET, anchor="center")

prediction_frame = tk.Frame(
    root,
    bg="white",
    width=420,
    height=95,
    highlightbackground="#cccccc",
    highlightthickness=1
)
prediction_frame.place(x=30, y=415 + OFFSET)

result_label = tk.Label(
    prediction_frame,
    text="",
    font=("Arial", 13, "bold"),
    bg="white",
    fg="green"
)

# disease info
info_title = tk.Label(root, text=translate("disease_info"),
                      font=("Arial", 14, "bold"), bg="#f2f2f2")
info_title.place(relx=0.5, y=520 + OFFSET + EXTRA, anchor="center")

info_text = tk.Text(root, wrap=tk.WORD, width=55, height=5,
                    bg="white", fg="black", font=("Arial", 11))
info_text.place(x=20, y=545 + OFFSET + EXTRA)

# advice
advice_title = tk.Label(root, text=translate("advice"),
                        font=("Arial", 14, "bold"), bg="#f2f2f2")
advice_title.place(relx=0.5, y=650 + OFFSET + EXTRA, anchor="center")

advice_text = tk.Text(root, wrap=tk.WORD, width=55, height=5,
                      bg="white", fg="black", font=("Arial", 11))
advice_text.place(x=20, y=675 + OFFSET + EXTRA)

# bottom buttons
bottom_frame = tk.Frame(root, bg="#f2f2f2")
bottom_frame.place(relx=0.5, rely=0.96, anchor="center")

btn1 = tk.Button(bottom_frame, text=translate("btn_shop"),
                 bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
                 width=18, height=1)
btn1.grid(row=0, column=0, padx=10)

btn2 = tk.Button(bottom_frame, text=translate("btn_chat"),
                 bg="#FF9800", fg="white", font=("Arial", 12, "bold"),
                 width=18, height=1)
btn2.grid(row=0, column=1, padx=10)

def run_app():
    root.mainloop()

if __name__ == "__main__":
    run_app()
