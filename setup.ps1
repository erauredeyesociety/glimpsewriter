# Define directories
$main_dir = "data"
$OCR_dir = "data\pdfs_4_OCR"

# Create directories
New-Item -ItemType Directory -Force -Path $main_dir
New-Item -ItemType Directory -Force -Path $OCR_dir

# Output creation message
Write-Output "Created $OCR_dir, , place your raw PDFs here..."

# Install requirements
pip install -r requirements.txt

# Output installation message
Write-Output "Installed requirements"

python -m spacy download en_core_web_sm

Write-Output "Downloaded spacy en_core_web_sm model"