# AgentForms

AgentForms is a Python project designed to interact with Google Sheets and Google Cloud Vision API, process images using OCR, and handle various image processing tasks.

## Features

- Read and write data to Google Sheets using `gspread`
- Authenticate securely with Google APIs using `google-auth`
- Perform Optical Character Recognition (OCR) on images with `pytesseract`
- Image processing capabilities powered by `Pillow`
- Integrate with Google Cloud Vision API for advanced image analysis
- Make HTTP requests easily with `requests`

## Requirements

The project dependencies are listed in `requirements.txt`:

- gspread==6.1.2
- google-auth==2.34.0
- pytesseract==0.3.13
- Pillow==10.2.0
- requests==2.32.3
- google-cloud-vision==3.7.2

Install them with:

```bash
pip install -r requirements.txt