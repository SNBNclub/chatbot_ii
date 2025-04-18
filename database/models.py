from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ARRAY, BigInteger, ForeignKey, Numeric, JSON, Date
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from instance import SQL_URL_RC

engine = create_async_engine(url=SQL_URL_RC, echo=True)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    name = Column(String, default='')
    is_superuser = Column(Boolean, default=False)


class CurDialog(Base):
    __tablename__ = 'cur_dialog'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    dialog_id = Column(Integer, ForeignKey('dialog.id'))


class Dialog(Base):
    __tablename__ = 'dialog'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dialog = Column(String, default='')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
