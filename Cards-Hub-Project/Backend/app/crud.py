from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine , async_sessionmaker
from sqlalchemy.orm import  Mapped , mapped_column , DeclarativeBase
from datetime import datetime
from Backend_planner.app.instance_password_page import TableFrameworkCO , TableCreateCardsCO , TableSignInCO
from sqlalchemy import select , ForeignKey , JSON

class AlchemyLaunch(DeclarativeBase):
    pass

class TableFrameworkDB(AlchemyLaunch):
    __tablename__ = 'password_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[str] = mapped_column(default=lambda: datetime.now().strftime("%d.%m.%Y %H:%M"))

class TableCreateCardsDB(AlchemyLaunch):
    __tablename__ = 'cards_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_email: Mapped[str] = mapped_column(ForeignKey('password_table.email',ondelete='CASCADE'))
    todo_column: Mapped[list[str]] = mapped_column(JSON,default=list)
    progress_column: Mapped[list[str]] = mapped_column(JSON,default=list)
    done_column: Mapped[list[str]] = mapped_column(JSON,default=list)

URL = 'postgresql+asyncpg://postgres:[WRITE HERE YOUR DB PASSWORD]@db_postgres:5432/[NAME OF YOUR DATABASE]'
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

async def get_user_email(email: str,session: AsyncSession):
    request = select(TableFrameworkDB).where(TableFrameworkDB.email == email)
    result = await session.execute(request)
    found_email = result.scalar_one_or_none()
    if found_email is None:
        return None
    return found_email

from sqlalchemy import update
async def update_user_password(nickname: str,new_hash: str,session: AsyncSession):
    request = update(TableFrameworkDB).where(TableFrameworkDB.nickname == nickname).values(password=new_hash)
    await session.execute(request)
    await session.commit()

async def store_cards(instance: TableCreateCardsCO,session: AsyncSession):
    validated_cards = TableCreateCardsDB(
                          user_email = instance.user_email,
                          todo_column = instance.todo_column,
                          progress_column = instance.progress_column,
                          done_column = instance.done_column
                                        )
    session.add_all([validated_cards])
    await session.commit()
    return {
        "status_code" : 201,
        "comment": "successful connection!"
    }

async def get_cards(email: str,session: AsyncSession):
    request = select(TableCreateCardsDB).where(TableCreateCardsDB.user_email == email)
    result = await session.execute(request)
    column_info = result.scalars().all()
    if not column_info:
        return {
            "todo_column" : [],
            "progress_column" : [],
            "done_column" : []
               }
    else:
        last_save = column_info[-1]
        return {
            "todo_column": last_save.todo_column,
            "progress_column": last_save.progress_column,
            "done_column": last_save.done_column
               }

from sqlalchemy import delete
async def drop_cards(email: str,session: AsyncSession):
    request = delete(TableCreateCardsDB).where(TableCreateCardsDB.user_email == email)
    await session.execute(request)
    await session.commit()
    return {'status_code' : 200,'comment' : 'Data was deleted successfully!'}

async def change_password(email: str,new_password: str,session: AsyncSession):
    request = update(TableFrameworkDB).where(TableFrameworkDB.email == email).values(password=new_password)
    await session.execute(request)
    await session.commit()
    return {'status_code': 200, 'comment': 'Password has been changed successfully!'}

