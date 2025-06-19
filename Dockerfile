# 1) Base image
FROM python:3.11-slim

# 2) Set working dir
WORKDIR /app

# 3) Install system deps for C extensions (WordCloud, Pillow, etc.) + sqlite
RUN apt-get update && \
    apt-get install -y \
      build-essential \
      python3-dev \
      libfreetype6-dev \
      pkg-config \
      sqlite3 \
      libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

# 4) Copy & install Python deps (cache-friendly)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m nltk.downloader vader_lexicon

# 5) Copy project & switch into src/
COPY . .
WORKDIR /app/src

# 6) Expose port & default command
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# # 7) Theme update 
# COPY .streamlit /app/.streamlit