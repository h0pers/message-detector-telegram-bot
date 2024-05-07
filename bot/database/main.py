from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from bot.config import DB_URL

engine = create_async_engine(DB_URL, echo=False)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass
