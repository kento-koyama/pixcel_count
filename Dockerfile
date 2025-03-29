FROM python:3.9-slim-buster

WORKDIR /app

# システムパッケージのインストール
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y \
        libgl1-mesa-glx \
        libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Pythonライブラリのインストール
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# アプリケーションのコピー
COPY . /app

EXPOSE 8080

ENTRYPOINT ["streamlit", "run"]
CMD ["main.py", "--server.port=8080"]
