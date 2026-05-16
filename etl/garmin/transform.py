import pandas as pd

def transform_activities(raw: list) -> pd.DataFrame:
    rows = []
    for a in raw:
        rows.append({
            "activity_id":     str(a.get("activityId", "")),
            "name":            a.get("activityName", ""),
            "activity_type":   a.get("activityType", {}).get("typeKey", ""),
            "start_time":      a.get("startTimeLocal", ""),
            "duration_secs":   a.get("duration", 0),
            "distance_meters": a.get("distance", 0),
            "avg_hr":          a.get("averageHR", None),
            "max_hr":          a.get("maxHR", None),
            "calories":        a.get("calories", 0),
            "avg_speed":       a.get("averageSpeed", None),
            "elevation_gain":  a.get("elevationGain", None),
        })
    df = pd.DataFrame(rows)
    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    df["distance_km"] = df["distance_meters"] / 1000
    df["duration_min"] = df["duration_secs"] / 60
    return df

def transform_steps(raw: list) -> pd.DataFrame:
    rows = []
    for day in raw:
        rows.append({
            "date":        day.get("calendarDate", ""),
            "total_steps": day.get("totalSteps", 0),
            "goal":        day.get("stepGoal", 0),
        })
    return pd.DataFrame(rows)

def transform_sleep(raw: list) -> pd.DataFrame:
    rows = []
    for entry in raw:
        summary = entry.get("dailySleepDTO", {})
        rows.append({
            "date":          summary.get("calendarDate", ""),
            "sleep_seconds": summary.get("sleepTimeSeconds", 0),
            "deep_seconds":  summary.get("deepSleepSeconds", 0),
            "light_seconds": summary.get("lightSleepSeconds", 0),
            "rem_seconds":   summary.get("remSleepSeconds", 0),
            "awake_seconds": summary.get("awakeSleepSeconds", 0),
            "score":         summary.get("sleepScores", {}).get("overall", {}).get("value", None),
        })
    return pd.DataFrame(rows)