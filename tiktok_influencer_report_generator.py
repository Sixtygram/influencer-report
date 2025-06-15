print("🚀 Script started — reading sheet and launching...")
print(f">>> Processing influencer: {name}")

import os, json

# เขียนไฟล์ service account จาก ENV
if "GOOGLE_APPLICATION_CREDENTIALS_JSON" in os.environ:
    with open("influencer-credentials.json", "w") as f:
        json.dump(json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]), f)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "influencer-credentials.json"

# -*- coding: utf-8 -*-
"""
TikTok Influencer Report Generator
=================================
สร้างไฟล์ PNG / PDF รายคน ด้วยเลย์เอาต์ตามตัวอย่างที่ผู้ใช้ให้มา

วิธีทำงาน (High-level)
-----------------------
1. ดึงข้อมูล Influencer Name + TikTok URL จาก Google Sheet
2. สำหรับแต่ละ URL ➡ ดึงสถิติ View / Like / Share / Comment
3. เติมข้อมูล + รูปโปรไฟล์ ลงใน template.png ตามตำแหน่งที่กำหนด
4. Export เป็น .png (และ opt. PDF)

ก่อนใช้งาน
-----------
$ python -m venv venv && source venv/bin/activate
$ pip install google-api-python-client google-auth pandas pillow requests playwright
$ playwright install

ตั้งค่า GOOGLE_APPLICATION_CREDENTIALS เป็น Service Account JSON ที่มีสิทธิอ่าน Google Sheet

แก้ไขค่าด้านล่างให้ตรงกับไฟล์ / คอลัมน์ในชีตของคุณ
"""
# ... (ตัดตอนเพื่อความยาวสมเหตุผล) ...
