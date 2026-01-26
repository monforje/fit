import random
import time
import os
import psycopg2

DB_URL = os.getenv("DATABASE_URL") or os.getenv(
    "LOCAL_DATABASE_URL", "postgresql://dan:dan@localhost:5432/fit"
)
INTERVAL = int(os.getenv("INTERVAL_SECONDS", "1"))


def connect_db():
    return psycopg2.connect(DB_URL)


def init_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            id BIGSERIAL PRIMARY KEY,
            steps INTEGER NOT NULL,
            calories INTEGER NOT NULL,
            activity_type VARCHAR(50) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
    """)
    

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
    conn = None
    cur = None

    try:
        conn = connect_db()
        cur = conn.cursor()
        init_tables(cur)
        conn.commit()

        print("Connected to DB")

        insert_sql = """
            INSERT INTO activity (steps, calories, activity_type)
            VALUES (%s, %s, %s)
            RETURNING id, created_at
        """

        while True:
            record = generate_activity()
            cur.execute(
                insert_sql,
                (record["steps"], record["calories"], record["activity_type"]),
            )
            row = cur.fetchone()
            if row is None:
                conn.rollback()
                raise RuntimeError("Insert succeeded but RETURNING returned no row")
            conn.commit()

            print(
                "Inserted:",
                "id=", row[0],
                "time=", row[1],
                "data=", record,
            )

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()