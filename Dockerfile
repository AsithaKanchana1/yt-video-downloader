# Dockerfile for YouTube Downloader & MP3 Converter

FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY youtube_converter.py .

# Install Python dependencies
# Using --no-cache-dir to reduce image size
# Install pytubefix instead of pytube
RUN pip install --no-cache-dir pytubefix moviepy==1.0.3 # <--- CHANGE HERE

CMD ["python", "-u", "./youtube_converter.py"]
