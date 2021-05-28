import os
from datetime import datetime


import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from io import StringIO

import ocrmypdf
import pdfplumber
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()


@app.get("/")
def index():
    return {"requests": "1. call '/get_doc_list' to get list of all documents available \n 2. call '/parse/<doc_name>' to get text content of document"}

@app.get("/get_doc_list")
def get_doc_list():
    ls = os.listdir("app/data")
    return {"doc_list": ls}

@app.get("/parse/{sample_doc}")
def get_text(sample_doc : str):
    path = "data/"+sample_doc+".pdf"
    response = jsonable_encoder(pdf_to_text(path))
    return JSONResponse(content = response)

def pdf_to_text(path):
    """
    returns json form of text extracted from pdf specified in the path
    response contains number of pages and text in each page
    """

    response = {}
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    info = doc.info[0].keys()
    dtformat = "%Y%m%d%H%M%S"

    response['Author'] = doc.info[0]["Author"].decode("utf-8") if "Author" in info else None
    response['Creator'] = doc.info[0]["Creator"].decode("utf-8") if "Creator" in info else None

    if "CreationDate" in info:
        clean_creation = doc.info[0]["CreationDate"].decode("utf-8").replace("D:","").split('+')[0]
        response['CreationDate'] = datetime.strptime(clean_creation, dtformat)
    else: None

    if "ModDate" in info:
        clean_modified = doc.info[0]["CreationDate"].decode("utf-8").replace("D:","").split('+')[0]
        response['LastModified'] = datetime.strptime(clean_modified, dtformat)
    else: None

    num_pages = 0

    for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
        interpreter.process_page(page)
        response['page_'+str(pageNumber)+"_text"] = retstr.getvalue().replace("-/n", "")
        if (len(response['page_'+str(pageNumber)+"_text"])) < 5:
            response['page_'+str(pageNumber)+"_text"] = image_to_text(path, pageNumber)
        retstr.truncate(0)
        retstr.seek(0)
        num_pages += 1

    response['num_pages'] = num_pages
    fp.close()
    device.close()
    retstr.close()
    return response

def image_to_text(path, pageNumber):
    os.system(f'ocrmypdf {path} output.pdf')
    text = ""
    with pdfplumber.open('output.pdf') as pdf:
        page = pdf.pages[pageNumber]
        text = page.extract_text(x_tolerance=2)
        print(text)
    return text