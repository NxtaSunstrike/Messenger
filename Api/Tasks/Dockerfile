FROM python:3.11.9

RUN mkdir /Faststream

WORKDIR /Faststream

COPY  requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000