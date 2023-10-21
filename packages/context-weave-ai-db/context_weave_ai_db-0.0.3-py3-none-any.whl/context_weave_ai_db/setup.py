import logging
import os
import psycopg2
from contextlib import contextmanager
from psycopg2.errors import DuplicateDatabase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Request, RequestByUrl


logger = logging.getLogger(__name__)


def create_db(db_name: str):
    # connection establishment
    conn = psycopg2.connect(
        database="postgres",
        user=os.getenv("POSTGRES_USER", default="postgres"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", default="localhost"),
        port=os.getenv("POSTGRES_PORT", default=5432),
    )

    conn.autocommit = True

    # Creating a cursor object
    cursor = conn.cursor()

    # query to create a database
    sql = f'''CREATE DATABASE {db_name}'''

    try:
        # executing above query
        cursor.execute(sql)
        logger.info("Database has been setup successfully!!")

        # Closing the connection
        conn.close()
    except DuplicateDatabase:
        pass


def get_engine():
    database = os.getenv("POSTGRES_DB_NAME")
    password = os.getenv("POSTGRES_PASSWORD")
    dialect = os.getenv("POSTGRES_DIALECT", default="postgresql")
    user = os.getenv("POSTGRES_USER", default="postgres")
    host = os.getenv("POSTGRES_HOST", default="localhost")
    port = os.getenv("POSTGRES_PORT", default=5432)
    uri = f"{dialect}://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url=uri)


def setup_tables():
    engine = get_engine()

    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    Request.__table__.create(bind=engine, checkfirst=True)
    RequestByUrl.__table__.create(bind=engine, checkfirst=True)


@contextmanager
def session_scope():
    Session = sessionmaker(bind=get_engine())
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def session_scope_select():
    Session = sessionmaker(bind=get_engine())
    session = Session()
    try:
        yield session
    except Exception:
        raise
    finally:
        session.close()
