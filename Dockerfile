FROM python:3.8-slim-buster
RUN apt update && apt install -y git libpq-dev gcc && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 -m sakura