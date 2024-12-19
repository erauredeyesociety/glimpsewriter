# Pass entire PDFs through OCR so that the text of the pdf can be easily selected, searched, or extracted 

'''
Some Setup

* Python Packages
    pip install ocrmypdf pytesseract camelot-py Pillow

* Install tesseract-ocr
    https://tesseract-ocr.github.io/tessdoc/Installation.html
* tesseract for windows
    https://github.com/UB-Mannheim/tesseract/wiki

* Install ghostscript under AGPL release
    https://ghostscript.com/releases/gsdnld.html

* Check ghostscript bin & lib folders in PATH
    Example - for windows
        C:\Program Files\gs\gs10.04.0\bin
        C:\Program Files\gs\gs10.04.0\lib
'''

import ocrmypdf
import pytesseract
import os
from tqdm import tqdm
from colorama import Fore

# Set tesseract command path
pytesseract.pytesseract.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd = ("C:\\Program Files\\Tesseract-OCR\\tesseract.exe")

def ocr(orig_file, new_file):
    # Perform OCR on the original PDF file and save the output
    ocrmypdf.ocr(orig_file, new_file, skip_text=True)  # Additional options can be added if needed

def check_path(folder_path):
    # Ensure folder path uses correct separator for the operating system
    if os.name == "nt":
        if folder_path[-1] != "\\":
            folder_path += "\\"
    else:
        if folder_path[-1] != "/":
            folder_path += "/"
    return folder_path

def pdf_2_ocr_run(input_dir, output_dir, tesseract_path):
    print(Fore.GREEN + "Processing PDFs through OCR..." + Fore.RESET)

    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    # Ensure the input and output paths are correctly formatted
    input_dir = check_path(input_dir)
    output_dir = check_path(output_dir)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Process each PDF file in the input folder
    files = [file for file in os.listdir(input_dir) if file.endswith(".pdf")]
    for file in tqdm(files, desc="Processing files", dynamic_ncols=True):
        # Update tqdm description with the file name (in blue)
        tqdm.write(f"{Fore.BLUE}Processing: {file}{Fore.RESET}")
        
        # Perform OCR on each PDF and save to the output folder
        ocr(os.path.join(input_dir, file), os.path.join(output_dir, file))

        # Log completed processing (in green)
        tqdm.write(f"{Fore.GREEN}Processed: {file}{Fore.RESET}")

#if __name__ == "__main__":
#    input_dir = "data/pdfs_4_OCR"  # Fixed input folder
#    output_dir = "data/pdfs_4_sentences"  # Fixed output folder
#    tesseract_path = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
#    pdf_2_ocr_run(input_dir, output_dir, tesseract_path)
