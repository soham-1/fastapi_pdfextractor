# fastapi_pdfextractor ![GitHub top language](https://img.shields.io/github/languages/top/soham-1/fastapi_pdfextractor?color=%2300ff00)
A simple api using [fastapi](https://pypi.org/project/fastapi/) for extracting the text content of pdf using [pdfminer](https://pypi.org/project/pdfminer/). 
Different pdf parsers were tried like pypdf2, pdfminer.. but pdfminer gave better results. For added ocr support first install [tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and [ghost script](https://www.ghostscript.com/download/gsdnld.html) as these are required dependencies for the code to work.<br>
Try out and compare the output of pdfminer and tika through API endpoints. Access the results through API response or app/results directory. 
<br>
Note: if tesseract is installed in some other location than default, then change the location accordingly in pdfapi.py file.

## Clone project
```
git clone https://github.com/soham-1/fastapi_pdfextractor.git
```

## Run locally
### Install dependencies
```
pip install -r requirements.txt
```

### Run Server
```
cd app
uvicorn pdfapi:app --host 0.0.0.0 --port 8000 --reload
```

## Run on Docker
```
docker-compose up -d --build
```

### Stop the container using
```
docker-compose stop fast_api
```

### Restart it using
```
docker-compose up -d
```

## Documentation
This api has following endpoints
* #### ```/get_doc_list``` - for getting a list of all the available pdf's
* #### ```/parse/{doc_name}``` - for getting the meta data and text content of pdf. available pdf's are sample_doc_1, sample_doc_2. sample_doc_3
* #### ```/pdfminer_text/{doc}``` - returns text output of a pdf using pdfminer library
* #### ```/pdfminer_text/{doc}/{page_no}``` - returns text output of a pdf of specified page_no
* #### ```/tika_text/{doc}``` - returns text output of a pdf using py-tika library
* #### ```/pdfminer_xml/{doc}``` - returns xml output
* #### ```/pdfminer_xml/{doc}/{page_no}``` - returns xml output of a pdf of specified page_no
* #### ```/pdfminer_html/{doc}``` - returns html output
* #### ```/pdfminer_html/{doc}/{page_no}```
* #### ```/pdfminer_html_char/{doc}``` - returns character level html output
* #### ```/pdfminer_html_char/{doc}/{page_no}```

### text pdf
![get_doc_list](/screenshots/get_doc_list.JPG)

### output
<img src="/screenshots/parse_doc_2.JPG" alt="parse doc" width="800" height="400">

### pdf with scanned image
<img src="/screenshots/doc_3.JPG" alt="parse doc" width="400" height="400">

### output
![get_doc_list](/screenshots/parse_doc_3.JPG)
