import os


from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"

async_engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
