from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine , async_sessionmaker
from sqlalchemy.orm import  Mapped , mapped_column , DeclarativeBase
from datetime import datetime
from Backend_password_page.app.instance_password_page import TableFrameworkCO , PresentCredentials
from sqlalchemy import select

class AlchemyLaunch(DeclarativeBase):
    pass

class TableFrameworkDB(AlchemyLaunch):
    __tablename__ = 'password_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[str] = mapped_column(default=lambda: datetime.now().strftime("%d.%m.%Y %H:%M"))

URL = 'postgresql+asyncpg://postgres:0631@localhost:5432/password_database'
engine_origin = create_async_engine(URL,echo=True)
session_origin = async_sessionmaker(engine_origin,expire_on_commit=False)

async def keep_open_database():
    async with session_origin() as session:
        yield session

async def create_password(instance: TableFrameworkCO,session: AsyncSession):
    validated_instance = TableFrameworkDB(nickname=instance.nickname,
                                          email=instance.email,
                                          password=instance.password
                                          )
    session.add_all([validated_instance])
    await session.commit()
    return {
        "status_code" : 201,
        "comment" : "successful connection!"
    }

async def return_to_account(instance: PresentCredentials,session: AsyncSession):
    nickname = instance.nickname
    password = instance.password
    request = select(TableFrameworkDB).where(TableFrameworkDB.nickname == nickname and TableFrameworkDB.password == password)
    search_result = await session.execute(request)
    user_data = search_result.scalar_one_or_none()
    if user_data is None:
        raise HTTPException(status_code=404,detail='nickname or password is incorrect')
    else:
        pass

