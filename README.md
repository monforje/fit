в корне делаем

python -m venv .venv

потом

.venv\Scripts\activate

потом

pip install sqlalchemy python-dotenv alembic

или

pip install -r requirements.txt

для выполения миграций используем

alembic upgrade head