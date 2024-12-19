# glimpsewriter
working to make summarizations out of novels.

## Dependencies

Need to install tesseract and ghostscript.

* Install [tesseract-ocr](https://tesseract-ocr.github.io/tessdoc/Installation.html)
  * tesseract [for windows](https://github.com/UB-Mannheim/tesseract/wiki)
* Install [ghostscript](https://ghostscript.com/releases/gsdnld.html) under AGPL release
  * Check ghostscript bin & lib folders in PATH
  * Example - for windows
    * > C:\Program Files\gs\gs10.04.0\bin
    * > C:\Program Files\gs\gs10.04.0\lib

Install pytorch for cuda 11.6

```bash
pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 -f https://download.pytorch.org/whl/cuda/11.6/torch_stable.html
```

## Data Organization / Directory Structure

All data stored in ./data/ folder

Pass pdfs through OCR

- put input PDFs in "pdfs_4_OCR" folder
- output PDFs will appear in "pdfs_4_sentences" folder

Convert PDFs to plain text sentences:

- put input PDFs in "pdfs_4_sentences" folder
- output text files will appear in "data_4_sumz" folder

Summarize PDFs:

- put intput data in "data_4_sumz" folder
- output summaries will appear in "data_sumz" folder
  - multiple summaries folders corresponding to model used to summarize data

Convert Summaries to Markdown

- put intput data in "data_sumz" folder
- output markdown will appear in "data_sumz_md" folder