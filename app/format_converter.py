import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from io import StringIO, BytesIO

from tika import parser

from bs4 import  BeautifulSoup


def pdfminer_to_text(input_file:str, page_no:int=None):
    file_loc = "app/data/" + input_file + ".pdf"
    fp = open(file_loc, 'rb')
    outfp = BytesIO()
    rsrcmgr = PDFResourceManager()
    laparams = LAParams(line_overlap=.5, char_margin=60, line_margin=.5, word_margin=1, boxes_flow=.6,
                            detect_vertical=True, all_texts=False)
    # laparams = LAParams() # default configurations
    device = TextConverter(rsrcmgr, outfp, 'utf-8', laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    text = ""
    for page_index, page in enumerate(PDFPage.get_pages(fp)):
        if page_no is None or page_index == page_no:
            interpreter.process_page(page)
            text += outfp.getvalue().decode()
            if page_no and page_index == page_no: break
    output_file = f'app/results/pdfminer_{input_file}.txt' if page_no is None else f'app/results/pdfminer_{input_file}_page{page_no}.txt'
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(text)
    return text


def tika_to_text(input_file):
    parsed_pdf = parser.from_file("app/data/" + input_file + ".pdf")
    text = parsed_pdf["content"]
    output_file = f'app/results/tika_{input_file}.txt'
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(text)
    return text


def pdfminer_to_xml(input_file:str, page_no:int=None):
    file_loc = "app/data/" + input_file + ".pdf"
    fp = open(file_loc, 'rb')
    outfp = BytesIO()
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = XMLConverter(rsrcmgr, outfp, 'utf-8', laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    text = ""
    for page_index, page in enumerate(PDFPage.get_pages(fp)):
        if page_no is None or page_index == page_no:
            interpreter.process_page(page)
            text += outfp.getvalue().decode()
            outfp.seek(0)
            outfp.truncate(0)
            if page_no and page_index == page_no: break
    output_file = f'app/results/pdfminer_{input_file}.xml' if page_no is None else f'app/results/pdfminer_{input_file}_page{page_no}.xml'
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(text)
    return text


def pdfminer_to_html(input_file:str, page_no:int=None):
    file_loc = "app/data/" + input_file + ".pdf"
    fp = open(file_loc, 'rb')
    outfp = BytesIO()
    rsrcmgr = PDFResourceManager()
    laparams = LAParams(line_overlap=.5, char_margin=60, line_margin=.5, word_margin=1, boxes_flow=.6,
                            detect_vertical=True, all_texts=False)
    # laparams = LAParams()
    device = HTMLConverter(rsrcmgr, outfp, 'utf-8', laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    text = ""
    for page_index, page in enumerate(PDFPage.get_pages(fp)):
        if page_no is None or page_index == page_no:
            interpreter.process_page(page)
            retstr = outfp.getvalue().decode()
            text += retstr
            output_file = f'app/results/pdfminer_{input_file}_page{page_index}.html'
            with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(retstr)
            if page_no and page_index == page_no: break
            outfp.seek(0)
            outfp.truncate(0)
    return text


def pdfminer_to_html_char_level(input_file:str, page_no:int=None):
    xml = pdfminer_to_xml(input_file, page_no)
    body_start = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
            .html, body{
                width: 100%;
                height: 100%;
            }
            </style>
            
        </head>
        <body>\n"""

    body_end = """\n</body>
        </html>"""    
        
    source = BeautifulSoup(xml, 'xml')
    pages = source.findAll("page")
    text_val = ""
    for page_index, page in enumerate(pages):
        output_file = f'app/results/pdfminer_char_{input_file}_page{page_index}.html'
        with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(body_start)
            page_width = page["bbox"].split(',')[2]
            page_height = page["bbox"].split(',')[3]
            textbox = page.findAll("text")
            for text in textbox:
                if "bbox" in text.attrs:
                    left, bottom, right, top = text.attrs['bbox'].split(',')
                    style = f"display:inline; position: absolute; left:{left}px; top:{round(float(page_height)-float(top),3)}px; font-size: {round(float(top)-float(bottom),3)}px; font-family: {text.attrs['font'].split('+')[1]};"
                    div = f"\n<div style='{style}'>{text.text}</div>"
                    text_val += div
                    f.write(div)
            f.write(body_end)
    return body_start + text_val + body_end