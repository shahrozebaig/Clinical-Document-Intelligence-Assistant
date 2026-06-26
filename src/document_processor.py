import os
import fitz
from src.ocr_processor import extract_text_from_image,extract_text_from_scanned_pdf

def extract_text_from_pdf(pdf_path):
    document=fitz.open(pdf_path)
    pages=[]
    for page_number,page in enumerate(document,start=1):
        text=page.get_text("text")
        if text.strip():
            pages.append({"page_number":page_number,"text":text})
    return pages

def process_document(file_path):
    extension=os.path.splitext(file_path)[1].lower()

    if extension==".txt":
        with open(file_path,"r",encoding="utf-8",errors="ignore") as file:
            text=file.read()
        return [{"page_number":1,"text":text}]

    if extension==".pdf":
        pages=extract_text_from_pdf(file_path)
        total_text=" ".join(page["text"] for page in pages)

        if len(total_text.strip())<50:
            pages=extract_text_from_scanned_pdf(file_path)

        return pages

    if extension in [".png",".jpg",".jpeg"]:
        text=extract_text_from_image(file_path)
        return [{"page_number":1,"text":text}]

    raise ValueError("Unsupported file type")