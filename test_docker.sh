#!/usr/bin/env bash
set -e
echo "Building Docker image..."
docker-compose build
echo "Starting container in detached mode..."
docker-compose up -d
echo "Waiting for Streamlit to be up (max 60s)..."
timeout=60
until curl -s http://localhost:8501 > /dev/null; do
  sleep 1
  ((timeout--))
  if [ $timeout -le 0 ]; then
    echo "Error: Streamlit did not start within 60 seconds." >&2
    docker-compose logs
    docker-compose down
    exit 1
  fi
done
echo "Success: Streamlit is running!"
docker-compose down
