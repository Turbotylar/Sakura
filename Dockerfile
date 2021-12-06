FROM python:3.8-slim-buster
ARG TARGETARCH
RUN apt update && apt install -y wget git gcc unzip libaio1 ffmpeg && rm -rf /var/lib/apt/lists/*
RUN { \
        echo "[architecture] [download url] [directory containing libs within zip]" ; \
        echo "amd64 https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basiclite-linux.x64-21.4.0.0.0dbru.zip instantclient_21_4"; \
        echo "arm64 https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-basiclite-linux.arm64-19.10.0.0.0dbru.zip instantclient_19_10"; \
        echo "386 https://download.oracle.com/otn_software/linux/instantclient/213000/instantclient-basiclite-linux-21.3.0.0.0.zip instantclient_21_3"; \
    } | grep ^${TARGETARCH} > oracle_source && \
    cat oracle_source && \
    wget "$(awk '{ print $2 }' oracle_source)" -O oracle_instantclient.zip && \
    mkdir /opt/oracle && \
    unzip oracle_instantclient.zip -d /opt/oracle && \
    mv "/opt/oracle/$(awk '{ print $3 }' oracle_source)" /opt/oracle/instantclient && \
    rm oracle_source oracle_instantclient.zip

ENV LD_LIBRARY_PATH="/opt/oracle/instantclient:${LD_LIBRARY_PATH}"

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "-m", "sakura"]