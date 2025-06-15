import os, json
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

def main():
    print("🚀 Script started — reading sheet and launching...")

    # เขียนไฟล์ service account จาก ENV
    if "GOOGLE_APPLICATION_CREDENTIALS_JSON" in os.environ:
        with open("influencer-credentials.json", "w") as f:
            json.dump(json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]), f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "influencer-credentials.json"

    # 📥 Debug: เริ่มเชื่อม Google Sheet
    print("📥 Connecting to Google Sheet...")

    # กำหนดข้อมูล Google Sheet
    SPREADSHEET_ID = "1vRr9RYRJWR46m_rnZoO37hHD96CwipECAIxbCeAsHUw"
    RANGE = "Selected KOLs!B:N"

    creds = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )

    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    print("✅ Connected to Google Sheet...")

    # แปลงเป็น DataFrame
    values = sheet.get("values", [])
    df = pd.DataFrame(values[1:], columns=values[0])  # ข้าม header

    # เริ่มอ่าน TikTok URL
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for i, row in df.iterrows():
            name = row["Influencers"]
            url = row["Link Post"]
            if not url:
                continue

            print(f">>> Processing influencer: {name}")
            print(f"🔗 Visiting TikTok URL: {url}")

            try:
                page.goto(url, timeout=15000)
                print(f"🌐 Loaded TikTok page for {name}")
                print("🔍 Extracting TikTok stats...")

                def extract_number(selector):
                    try:
                        text = page.locator(selector).first.text_content()
                        return text.strip() if text else "N/A"
                    except:
                        return "N/A"

                views = extract_number('strong[data-e2e="video-views"]')
                likes = extract_number('strong[data-e2e="like-count"]')
                shares = extract_number('strong[data-e2e="share-count"]')
                comments = extract_number('strong[data-e2e="comment-count"]')

                print(f"✅ Stats for {name}: Views={views}, Likes={likes}, Comments={comments}, Shares={shares}")

                # ถ้ามีฟังก์ชัน generate_report(name, username, views, likes, comments, shares)
                # ให้เรียกตรงนี้ได้เลย

            except Exception as e:
                print(f"❌ Failed to load TikTok for {name}: {e}")
                continue

if __name__ == "__main__":
    print("🔥 Running __main__")
    main()
