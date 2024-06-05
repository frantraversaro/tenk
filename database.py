from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from decouple import config

# Credentials
redshift_endpoint = config('redshift_endpoint')
redshift_port = config('redshift_port')
redshift_dbname = config('redshift_dbname')
redshift_user = config('redshift_user')
redshift_password = config('redshift_password')

connection_string = (
    f"redshift+psycopg2://{redshift_user}:{redshift_password}@{redshift_endpoint}:{redshift_port}/{redshift_dbname}"
)

engine = create_engine(connection_string)

SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()


def create_tables():
    # Drop tables if they exist (for demonstration purposes, be careful with this in production)
    Base.metadata.drop_all(bind=engine)
    # Create all tables
    Base.metadata.create_all(bind=engine)