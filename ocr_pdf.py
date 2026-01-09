import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np

# ================== CẤU HÌNH ==================
PDF_DIR = "data_pdfs"
OUT_DIR = "ocr_texts"

POPPLER_PATH = r"D:\poppler-25.12.0\Library\bin"
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA_DIR = r"C:\Program Files\Tesseract-OCR\tessdata"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR

os.makedirs(OUT_DIR, exist_ok=True)

# ================== TIỀN XỬ LÝ ẢNH ==================
def preprocess_image(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    gray = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]
    return Image.fromarray(gray)

# ================== OCR PDF ==================
def ocr_pdf(pdf_path):
    pages = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=POPPLER_PATH
    )

    full_text = []

    for i, page in enumerate(pages, 1):
        img = preprocess_image(page)
        text = pytesseract.image_to_string(
            img,
            lang="vie",
            config="--oem 3 --psm 6"
        )
        full_text.append(f"\n--- Trang {i} ---\n{text}")

    return "\n".join(full_text)

# ================== CHẠY OCR ==================
for file in os.listdir(PDF_DIR):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(PDF_DIR, file)
        print(f"🔍 OCR: {file}")

        text = ocr_pdf(pdf_path)

        if len(text.strip()) > 200:
            out_file = os.path.join(OUT_DIR, file.replace(".pdf", ".txt"))
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ Lưu: {out_file}")
        else:
            print("⚠ Văn bản quá ngắn, kiểm tra PDF")

print("🎉 OCR HOÀN TẤT")
