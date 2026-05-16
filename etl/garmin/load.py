import pandas as pd
from database.database import get_connection

def load_activities(df: pd.DataFrame):
    if df.empty:
        return
    cols = ["activity_id","name","activity_type","start_time",
            "duration_secs","distance_meters","avg_hr","max_hr",
            "calories","avg_speed","elevation_gain"]
    conn = get_connection()
    
    # Only insert rows that don't already exist
    existing = pd.read_sql("SELECT activity_id FROM activities", conn)
    new_rows = df[~df["activity_id"].isin(existing["activity_id"])]
    
    if not new_rows.empty:
        new_rows[cols].to_sql("activities", conn, if_exists="append", index=False)
        print(f"✅ Inserted {len(new_rows)} new activities.")
    else:
        print("ℹ️ No new activities to insert.")
    
    conn.close()

def load_steps(df: pd.DataFrame):
    if df.empty:
        return
    conn = get_connection()
    df.to_sql("daily_steps", conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ Loaded {len(df)} days of step data.")

def load_sleep(df: pd.DataFrame):
    if df.empty:
        return
    conn = get_connection()
    df.to_sql("sleep", conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ Loaded {len(df)} days of sleep data.")