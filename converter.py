from fastapi import FastAPI, UploadFile, File
from pdf2docx import Converter
import os

app = FastAPI()
print('hello')
@app.get("/")
def read_root():
    return {"message": "Hello, World"}


@app.post("/convert/")
async def convert_pdf_to_docx(file: UploadFile):
    # Ensure the uploaded file is a PDF
    if not file.filename.endswith(".pdf"):
        return {"error": "File must be in PDF format"}

    # Create a temporary directory to store the converted DOCX file
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Create paths for the uploaded and converted files
    pdf_path = os.path.join(temp_dir, file.filename)
    docx_path = os.path.join(temp_dir, file.filename.replace(".pdf", ".docx"))

    # Save the uploaded PDF to a temporary file
    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(file.file.read())

    # Convert the PDF to DOCX
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()

    # Return the path to the converted DOCX file
    return {"docx_file_path": docx_path}
    
