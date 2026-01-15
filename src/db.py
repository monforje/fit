from sqlalchemy import create_engine, text


class Database:
    def __init__(self, url: str):
        self.url = url
        self.engine = create_engine(url, pool_pre_ping=True, future=True)


def connect_database(url: str) -> Database:
    return Database(url)


def healthcheck(db: Database) -> None:
    with db.engine.connect() as conn:
        conn.execute(text("SELECT 1"))
