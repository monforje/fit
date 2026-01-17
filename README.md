Комаров Даниил
Б9123-09.03.04
Аналитика Данных

Как запустить:

python -m venv .venv в корне

.venv\Scripts\activate

pip install -r requirements.txt

alembic upgrade head

устанавливаем докер

копируем переменные из .env.example в .env
POSTGRES_USER=dan
POSTGRES_PASSWORD=dan
POSTGRES_DB=fit
DATABASE_URL=postgresql://dan:dan@postgres:5432/fit
LOCAL_DATABASE_URL=postgresql://dan:dan@localhost:5432/fit

REDASH_POSTGRES_USER=redash
REDASH_POSTGRES_PASSWORD=redash
REDASH_POSTGRES_DB=redash

REDASH_COOKIE_SECRET=put_some_long_random_string_here
REDASH_SECRET_KEY=put_some_long_random_string_here_too

INTERVAL_SECONDS=1
PYTHONUNBUFFERED=1

JUPYTER_TOKEN=dev

пишем docker-compose up в консоль

пишем docker-compose run -rm redash_server create_db

еще раз docker-compose up

Описание проекта:

end-to-end система, которая генерирует данные с фитнесс браслета, используя generator.py - генератор, основанный на таблице
ACTIVITY_PROFILES = {
    "walking":  {"steps_min": 200, "steps_max": 1400, "kcal_min": 0.03, "kcal_max": 0.06},
    "running":  {"steps_min": 500, "steps_max": 2500, "kcal_min": 0.06, "kcal_max": 0.11},
    "cycling":  {"steps_min": 0,   "steps_max": 200,  "kcal_min": 0.00, "kcal_max": 0.02},
    "gym":      {"steps_min": 50,  "steps_max": 600,  "kcal_min": 0.04, "kcal_max": 0.09},
},
сохраняет их и позволяет анализировать через Redash и Jupyter Notebook.
Есть миграции через alembic
Общий docker-compose

скриншот Data Source из Redash:
![alt text](screenshots/image4.png)

скриншоты работы redash с дашбордом:
![alt text](screenshots/image.png)

скриншот визуализации "Топ типов активности"
![alt text](screenshots/image1.png)
SELECT
  activity_type,
  COUNT(*)      AS records,
  SUM(steps)    AS steps_sum,
  SUM(calories) AS calories_sum
FROM activity
GROUP BY 1
ORDER BY steps_sum DESC;

скриншот визуализации "Активность по часам"
![alt text](screenshots/image2.png)
SELECT
  date_trunc('minute', created_at) AS minute,
  SUM(steps)    AS steps_sum,
  SUM(calories) AS calories_sum,
  AVG(steps)    AS steps_avg,
  AVG(calories) AS calories_avg
FROM activity
WHERE created_at >= now() - interval '60 minutes'
GROUP BY 1
ORDER BY 1;

скриншот визуализации "Последние записи"
![alt text](screenshots/image3.png)
SELECT
  id,
  created_at,
  activity_type,
  steps,
  calories
FROM activity
ORDER BY created_at DESC
LIMIT 50;

SQL:
Таблица:
id	bigint Автоматическое приращение [nextval('activity_id_seq')]	
steps	integer	
calories	integer	
activity_type	character varying(50)	
created_at	timestamptz [now()]

