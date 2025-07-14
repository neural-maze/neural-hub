from pdf2image import convert_from_path
import os
from dotenv import load_dotenv

load_dotenv(".env")

DATA_FOLDER_PATH = os.getenv("DATA_FOLDER_PATH")

PDF_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, "pdf")
PNG_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, "png")

for pdf_file in os.listdir(PDF_FOLDER_PATH):

    if pdf_file.lower().endswith(".pdf"):
        
        pdf_path = os.path.join(PDF_FOLDER_PATH, pdf_file)
        pdf_base_name = os.path.splitext(pdf_file)[0]
        
        try:
            pages = convert_from_path(pdf_path, dpi=200)

            for i, page in enumerate(pages, start=1):
                output_filename = f"{pdf_base_name}_{i}.png"
                output_path = os.path.join(PNG_FOLDER_PATH, output_filename)
                page.save(output_path, "PNG")
                print(f"Saved: {output_filename}")
        except Exception as e:
            print(f"Processing error: {pdf_file}: {e}")
