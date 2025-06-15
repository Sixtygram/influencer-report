FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip fonts-liberation libnss3 libatk-bridge2.0-0 \
    libxss1 libgtk-3-0 libasound2 libgbm1 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright + Python packages
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install --with-deps

# Copy source code
COPY . /app
WORKDIR /app

CMD ["python", "tiktok_influencer_report_generator.py"]
