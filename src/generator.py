import random
import time
from sqlalchemy import text

from config import load_settings
from db import connect_database, healthcheck


ACTIVITY_PROFILES = {
    "walking":  {"steps_min": 200, "steps_max": 1400, "kcal_min": 0.03, "kcal_max": 0.06},
    "running":  {"steps_min": 500, "steps_max": 2500, "kcal_min": 0.06, "kcal_max": 0.11},
    "cycling":  {"steps_min": 0,   "steps_max": 200,  "kcal_min": 0.00, "kcal_max": 0.02},
    "gym":      {"steps_min": 50,  "steps_max": 600,  "kcal_min": 0.04, "kcal_max": 0.09},
}


def generate_activity() -> dict:
    activity_type = random.choices(
        ["walking", "running", "cycling", "gym"],
        weights=[55, 15, 10, 20],
        k=1
    )[0]

    profile = ACTIVITY_PROFILES[activity_type]

    steps = random.randint(profile["steps_min"], profile["steps_max"])
    calories = steps * random.uniform(profile["kcal_min"], profile["kcal_max"])

    if activity_type == "cycling" or activity_type == "gym":
        calories += random.uniform(20, 180)

    return {
        "steps": steps,
        "calories": int(round(calories)),
        "activity_type": activity_type,
    }


def main():
    settings = load_settings()

    db = connect_database(settings.database_url)
    healthcheck(db)

    print("Connected to DB")

    insert_sql = text("""
        INSERT INTO activity (steps, calories, activity_type)
        VALUES (:steps, :calories, :activity_type)
        RETURNING id, created_at
    """)

    try:
        while True:
            record = generate_activity()

            with db.engine.begin() as conn:
                row = conn.execute(insert_sql, record).mappings().one()

            print("Inserted:",
                  "id=", row["id"],
                  "time=", row["created_at"],
                  "data=", record)

            time.sleep(settings.interval_seconds)

    except KeyboardInterrupt:
        print("Stopped by user")


if __name__ == "__main__":
        main()