import os
from datetime import date, timedelta
from dotenv import load_dotenv
from garminconnect import Garmin

load_dotenv()

def get_client():
    email    = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    client   = Garmin(email, password)
    client.login()
    print("✅ Logged in to Garmin Connect.")
    return client

def extract_activities(client, limit=50):
    print(f"📥 Extracting last {limit} activities...")
    return client.get_activities(0, limit)

def extract_steps(client, days=30):
    print(f"📥 Extracting step data for last {days} days...")
    end   = date.today()
    start = end - timedelta(days=days)
    return client.get_steps_data(start.isoformat(), end.isoformat())

def extract_sleep(client, days=30):
    print(f"📥 Extracting sleep data for last {days} days...")
    results = []
    for i in range(days):
        day = date.today() - timedelta(days=i)
        try:
            data = client.get_sleep_data(day.isoformat())
            if data:
                results.append(data)
        except Exception:
            pass
    return results