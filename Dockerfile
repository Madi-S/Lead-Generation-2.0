FROM python:3.12.1

RUN mkdir -p /usr/src/lead-generation/app
WORKDIR /usr/src/lead-generation/app

RUN pip install --upgrade pip
COPY /project/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "/project/main.py"]
