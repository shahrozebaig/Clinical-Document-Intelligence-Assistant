import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def extract_text_from_image(image_path):
    image=Image.open(image_path)
    return pytesseract.image_to_string(image)

def extract_text_from_scanned_pdf(pdf_path):
    pages=convert_from_path(pdf_path)
    results=[]
    for page_number,page in enumerate(pages,start=1):
        text=pytesseract.image_to_string(page)
        if text.strip():
            results.append({"page_number":page_number,"text":text})
    return results