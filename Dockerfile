FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
      build-essential \
      python3-dev \
      libfreetype6-dev \
      pkg-config \
      sqlite3 \
      libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m nltk.downloader vader_lexicon

COPY . .
WORKDIR /app/src

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]