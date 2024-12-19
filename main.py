# main.py

from src.pdf_2_ocr import pdf_2_ocr_run
from src.ocr_2_text import ocr_2_text_run
from src.text_2_sumz import text_2_sumz_run
from src.sumz_2_md import sumz_2_md_run

import os

data_dir = "data"
pdf2ocr_input = os.path.join(data_dir, "pdfs_4_OCR")
pdf2ocr_output = os.path.join(data_dir, "pdfs_4_sentences")
ocr2text_input = os.path.join(data_dir, "pdfs_4_sentences")
ocr2text_output = os.path.join(data_dir, "data_4_sumz")
text2sumz_input = os.path.join(data_dir, "data_4_sumz")
text2sumz_output = os.path.join(data_dir, "data_sumz")
sumz2md_input = os.path.join(data_dir, "data_sumz")
sumz2md_output = os.path.join(data_dir, "data_sumz_md")

pytesseract_location = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

if __name__ == "__main__":
    pdf_2_ocr_run(pdf2ocr_input, pdf2ocr_output, pytesseract_location)
    ocr_2_text_run(ocr2text_input, ocr2text_output)
    text_2_sumz_run(text2sumz_input, text2sumz_output)
    sumz_2_md_run(sumz2md_input, sumz2md_output)
