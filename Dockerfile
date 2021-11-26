FROM python:3.8-slim-buster
RUN apt update && apt install -y git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "-m", "sakura"]