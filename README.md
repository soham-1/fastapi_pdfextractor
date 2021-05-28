# fastapi_pdfextractor
A simple api using [fastapi](https://pypi.org/project/fastapi/) for extracting the text content of pdf using [pdfminer](https://pypi.org/project/pdfminer/). 
Different pdf parsers were tried like pypdf2, pdfminer.. but pdfminer gave better results. For added ocr support first install [tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and [ghost script](https://www.ghostscript.com/download/gsdnld.html) as these are required dependencies for the code to work.
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
This api has 2 endpoints
* /get_doc_list - for getting a list of all the available pdf's
* /parse/<doc_name> - for getting the meta data and text content of pdf. available pdf's are sample_doc_1, sample_doc_2. sample_doc_3

### text pdf
![get_doc_list](/screenshots/get_doc_list.JPG)

### output
<img src="/screenshots/parse_doc_2.JPG" alt="parse doc" width="800" height="400">

### pdf with scanned image
<img src="/screenshots/doc_3.JPG" alt="parse doc" width="400" height="400">

### output
![get_doc_list](/screenshots/parse_doc_3.JPG)
