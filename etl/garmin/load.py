import pandas as pd
from db.database import get_connection

def load_activities(df: pd.DataFrame):
    if df.empty:
        return
    cols = ["activity_id","name","activity_type","start_time",
            "duration_secs","distance_meters","avg_hr","max_hr",
            "calories","avg_speed","elevation_gain"]
    conn = get_connection()
    df[cols].to_sql("activities", conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ Loaded {len(df)} activities.")

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