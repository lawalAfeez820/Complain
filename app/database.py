

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel.ext.asyncio.session import  AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import Setting

Setting = Setting()
#use in heroku
DATABASE_URL = f"postgresql+{Setting.database_driver}://{Setting.database_username}:{Setting.database_password}@{Setting.database_host}:{Setting.database_port}/{Setting.database_name}"


engine = create_async_engine(DATABASE_URL, future=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session = sessionmaker(engine,class_= AsyncSession,expire_on_commit= False)
    async with async_session() as session:
        yield session