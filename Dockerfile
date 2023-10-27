FROM python:3.9

WORKDIR /application

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "application.py"]