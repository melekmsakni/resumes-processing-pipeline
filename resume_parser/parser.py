import io
import os
import docx2txt
import pdfplumber
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError
import pdf2image
import pytesseract
# from multiprocessing import Pool
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import logging
import mimetypes


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("parser.log"),  # Log to a file
        logging.StreamHandler()            # Also log to console
    ]
)

logger = logging.getLogger(__name__)

parser = FastAPI()

output_folder = "temp_text"

def is_pdf_image_based(pdf_path):
    try:
        """Check if a PDF is image-based by analyzing its first page."""
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            if text.strip():  # If there's any text, it's not image-based
                return False
            return True
    except Exception as e :
        logging.error(f'error while checking if image based file {pdf_path} : {str(e)} ')
        return 



def extract_text_from_image_pdf(pdf_path):
    """Extract text from a scanned PDF using OCR."""
    try:
        images = pdf2image.convert_from_path(pdf_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image, config='-c preserve_interword_spaces=1')
        return text
    except Exception as e :
        logging.error(f'error while  extract_text_from_image_pdf file {pdf_path} : {str(e)} ')
        return 



def extract_text_from_text_pdf(pdf_path):
    def extract_text(pdf_path):
        with open(pdf_path, 'rb') as fh:
            try:
                for page in PDFPage.get_pages(
                        fh,
                        caching=True,
                        check_extractable=True
                ):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(
                        resource_manager,
                        fake_file_handle,
                        codec='utf-8',
                        laparams=LAParams()
                    )
                    page_interpreter = PDFPageInterpreter(
                        resource_manager,
                        converter
                    )
                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()
                    yield text

                    # close open handles
                    converter.close()
                    fake_file_handle.close()
            except PDFSyntaxError:
                return
    
    try:
        raw_text_generator = extract_text(pdf_path)
        combined_text = ' '.join(page_text for page_text in raw_text_generator)
        return combined_text
    except Exception as e :
        logging.error(f'error while extract_text_from_text_pdf file {pdf_path} : {str(e)} ')
        return 


def extract_text_from_docx(docx_path):
    """Extract text from DOCX files using docx2txt."""
    try:
        return docx2txt.process(docx_path)
    except Exception as e:
        logging.error(f"Error reading DOCX file {docx_path}: {e}")
        return 


def extract_text_resume(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type=='application/pdf' :
        if is_pdf_image_based(file_path):
            return extract_text_from_image_pdf(file_path)
        else:
            return extract_text_from_text_pdf(file_path)
    elif mime_type=='application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return extract_text_from_docx(file_path)
    else:
        logging.error(f"Unsupported file format: {file_path}")
        return 


def parse_resume(file_path):
    try:
        text = extract_text_resume(file_path)
        if text is None :
            logging.error("text unavailable ")
            return
        with open(f'{output_folder}/{os.path.basename(file_path)}.txt', "w", encoding="utf-8") as f:
            f.write(text)
        return generate_from_text(text)
    except Exception as e:
        logging.error(f"Error parsing file {file_path}: {e}")

def generate_from_text(raw_text):
    # it will return json 
    return {'json':'content'}


# def resume_to_text(files_list):


#     os.makedirs(output_folder, exist_ok=True)
#     # for file in files_list:
#     #     write_file(file)
#     print('inside resume to text')
#     # write_file(files_list[0])
#     # with Pool(1) as p:
#     #     p.map(write_file, files_list)
    
#     return output_folder 

@parser.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    """Endpoint to upload a resume and convert it to text."""
    os.makedirs(output_folder, exist_ok=True)

    file_path = os.path.join(output_folder, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    json_resume = parse_resume(file_path)  # Process the file
    if json_resume is None :
        logger.error(f"could not process the file {file_path} ") 
    return JSONResponse(content={"message": "File processed successfully", "json_resume": json_resume})

