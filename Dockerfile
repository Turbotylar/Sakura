FROM python:3.8-slim-buster
RUN apt update && apt install -y wget git gcc && rm -rf /var/lib/apt/lists/*
RUN wget https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-basic-linux.${TARGETARCH/amd64/x64}-19.10.0.0.0dbru.zip && \
    mkdir /opt/oracle && \
    unzip instantclient-basiclite-*-19.10.0.0.0dbru.zip -d /opt/oracle

ENV LD_LIBRARY_PATH="/opt/oracle/instantclient_19_10:${LD_LIBRARY_PATH}"

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "-m", "sakura"]