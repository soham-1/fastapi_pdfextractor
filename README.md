# fastapi_pdfextractor
A simple api using [fastapi](https://pypi.org/project/fastapi/) for extracting the text content of pdf using [pdfminer](https://pypi.org/project/pdfminer/). 
Different pdf parsers were tried like pypdf2, pdfminer.. but pdfminer gave better results

## Clone project
```
git clone https://github.com/soham-1/fastapi_pdfextractor.git
```

## Run on Docker
```
docker-compose up -d --build
```
## Run locally
### Install dependencies
```
pip install -r requirements.txt
```

### Run Server
```
uvicorn app.pdfapi:app --host 0.0.0.0 --port 8000 --reload
```
## Documentation
This api has 2 endpoints
* /get_doc_list - for getting a list of all the available pdf's
* /parse/<doc_name> - for getting the meta data and text content of pdf. available pdf's are sample_doc_1, sample_doc_2. sample_doc_3

![get_doc_list](/screenshots/get_doc_list.JPG)

![parse doc](/screenshots/parse_doc_2.JPG)