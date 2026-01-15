в корне делаем (для локальной разработки)

python -m venv .venv

потом

.venv\Scripts\activate

потом

pip install sqlalchemy python-dotenv alembic psycopg2

или

pip install -r requirements.txt

для выполения миграций используем

alembic upgrade 

для запуска приложения

docker compose up -d