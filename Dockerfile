FROM python:3.8-slim-buster
RUN apt install -y git
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 .