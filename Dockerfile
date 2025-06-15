FROM python:3.12-slim

# ติดตั้ง dependency ที่ Playwright ต้องใช้
RUN apt-get update && apt-get install -y \
    wget gnupg unzip fonts-liberation libnss3 libatk-bridge2.0-0 \
    libxss1 libgtk-3-0 libasound2 libgbm1 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# ตั้ง working directory
WORKDIR /app

# คัดลอกไฟล์ทั้งหมดเข้า container
COPY . /app


# อัปเดต pip และติดตั้ง package
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ติดตั้ง Playwright และ browser
RUN playwright install --with-deps

# รัน Python script
CMD ["python", "tiktok_influencer_report_generator.py"]
