FROM python:3.8

RUN pip install fastapi uvicorn pdfminer

COPY ./app ./

CMD ["uvicorn", "app.pdfapi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]