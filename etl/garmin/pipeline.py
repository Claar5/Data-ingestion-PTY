from db.database import init_db
from etl.extract import get_client, extract_activities, extract_steps, extract_sleep
from etl.transform import transform_activities, transform_steps, transform_sleep
from etl.load import load_activities, load_steps, load_sleep

def run():
    print("🚀 Starting Garmin ETL pipeline...\n")
    init_db()

    client = get_client()

    # Activities
    raw_activities = extract_activities(client, limit=100)
    df_activities  = transform_activities(raw_activities)
    load_activities(df_activities)

    # Steps
    raw_steps = extract_steps(client, days=30)
    df_steps  = transform_steps(raw_steps)
    load_steps(df_steps)

    # Sleep
    raw_sleep = extract_sleep(client, days=30)
    df_sleep  = transform_sleep(raw_sleep)
    load_sleep(df_sleep)

    print("\n✅ ETL pipeline complete.")

if __name__ == "__main__":
    run()