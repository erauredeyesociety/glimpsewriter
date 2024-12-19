#!/bin/bash

main_dir="data"
OCR_dir="data/pdfs_4_OCR"

mkdir $main_dir
mkdir $OCR_dir

echo "Created ${OCR_dir}, place your raw PDFs here..."

pip install -r requirements.txt

echo "Installed requirements"

python -m spacy download en_core_web_sm

echo "Downloaded spacy en_core_web_sm model"