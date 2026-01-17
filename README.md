# Аналитика Данных - Фитнес Трекер

**Автор:** Комаров Даниил  
**Группа:** Б9123-09.03.04  
**Дисциплина:** Аналитика Данных

---

## Описание проекта

End-to-end система для генерации и анализа данных фитнес-браслета. Проект включает:

- **Генератор данных** (`generator.py`) - симулирует активность на основе профилей:
  ```python
  ACTIVITY_PROFILES = {
      "walking":  {"steps_min": 200, "steps_max": 1400, "kcal_min": 0.03, "kcal_max": 0.06},
      "running":  {"steps_min": 500, "steps_max": 2500, "kcal_min": 0.06, "kcal_max": 0.11},
      "cycling":  {"steps_min": 0,   "steps_max": 200,  "kcal_min": 0.00, "kcal_max": 0.02},
      "gym":      {"steps_min": 50,  "steps_max": 600,  "kcal_min": 0.04, "kcal_max": 0.09},
  }
  ```
- **База данных PostgreSQL** с миграциями через Alembic
- **Аналитика** через Redash и Jupyter Notebook
- **Оркестрация** через Docker Compose

---

## Структура базы данных

### Таблица `activity`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | bigint | Автоматическое приращение [nextval('activity_id_seq')] |
| `steps` | integer | Количество шагов |
| `calories` | integer | Сожженные калории |
| `activity_type` | varchar(50) | Тип активности |
| `created_at` | timestamptz | Время создания записи [now()] |

---

## Как запустить

### 1. Настройка Python (локального) окружения

*В приниципе может быть не нужно

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
```

### 2. Установка Docker

Убедитесь, что Docker Desktop установлен и запущен.

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
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
```

### 4. Запуск сервисов

```bash
docker-compose up
```

### 5. Инициализация базы данных Redash

*Сейчас благодаря init-db этого не нужно

```bash
docker-compose run --rm redash_server create_db
```

### 6. Перезапуск сервисов

```bash
docker-compose up
```

---

## Визуализации в Redash

### Data Source
![Data Source](screenshots/image4.png)

### Дашборд
![Дашборд](screenshots/image.png)

### Визуализация "Топ типов активности"
![Топ типов активности](screenshots/image1.png)

**SQL запрос:**
```sql
SELECT
  activity_type,
  COUNT(*)      AS records,
  SUM(steps)    AS steps_sum,
  SUM(calories) AS calories_sum
FROM activity
GROUP BY 1
ORDER BY steps_sum DESC;
```

### Визуализация "Активность по часам"
![Активность по часам](screenshots/image2.png)

**SQL запрос:**
```sql
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
```

### Визуализация "Последние записи"
![Последние записи](screenshots/image3.png)

**SQL запрос:**
```sql
SELECT
  id,
  created_at,
  activity_type,
  steps,
  calories
FROM activity
ORDER BY created_at DESC
LIMIT 50;
```

