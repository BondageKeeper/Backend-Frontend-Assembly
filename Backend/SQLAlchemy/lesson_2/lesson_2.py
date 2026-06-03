#delete is very similar to update , at the beginning we find SPECIFIC user in db and after we delete him/her from session , example:
#class User(ParentClass):
#    __tablename__ = 'ai_requests'
#    id: Mapped[int] = mapped_column(primary_key=True)
#    user_id: Mapped[int]
#    prompt: Mapped[str]
#
#async def delete_user_by_id(user_id: int):
#    async with async_session() as session:
#        query = select(User).where(User.id == user_id)
#        result = await session.execute(query)
#        user = result.scalar_one_or_none()
#        if user:
#            await session.delete(user)
#            await session.commit()
#
#also we can create relations between tables using external key - ForeignKey which refers (the column in daughter-table will have it)
#from sqlalchemy import ForeignKey
#class Base(DeclarativeBase):
#    pass
#
#
#from sqlalchemy import ForeignKey
#from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
#
#
#class Base(DeclarativeBase):
#    pass
#
#class User(Base):
#    __tablename__ = "users"
#    id: Mapped[int] = mapped_column(primary_key=True)
#    username: Mapped[str] = mapped_column(unique=True)
#    requests: Mapped[list["AIRequest"]] = relationship(back_populates="user")
#
#class AIRequest(Base):
#    __tablename__ = "ai_requests"
#    id: Mapped[int] = mapped_column(primary_key=True)
#    prompt: Mapped[str] = mapped_column()
#    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
#    user: Mapped["User"] = relationship(back_populates="requests")
#
#explanation : Foreign key simply connects two tables , nut what if we want to get posts of user after establishing this relation
#we of course should make a query with boring conditions we tell python 'go to the database, find table of posts , take all strings
#where user_id == 5 - and every time it repeats
#relationship tells python: 'I know that in db there is ForeignKey so check user_id on your own and gather all posts
#and pack them in beautiful python list'

#TASK_1:
import asyncio
from faker import Faker
fake = Faker('en_US')
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import async_sessionmaker , create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
DATABASE_TRY_URL = 'postgresql+asyncpg://postgres:0631@127.0.0.1:5432/try308'
engine = create_async_engine(DATABASE_TRY_URL,echo=True)
async_session = async_sessionmaker(engine,expire_on_commit=False)
class MainClass(DeclarativeBase):
    pass
class Users(MainClass):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    agents: Mapped[list['AIAgent']] = relationship(back_populates='user')

class AIAgent(MainClass):
    id: Mapped[int] = mapped_column(primary_key=True)
    __tablename__ = 'ai_agents'
    role: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id',ondelete="CASCADE"))
    user: Mapped['Users'] = relationship(back_populates='agents')

async def main():
    async with engine.begin() as structure_connection:
        await structure_connection.run_sync(MainClass.metadata.create_all)
    async with async_session() as session:
        my_user = Users(id = fake.random_int(min=1,max=999),
                         username='Ivan')
        new_prompt = AIAgent(role='efficient')
        my_user.agents.append(new_prompt)
        session.add_all([my_user])
        await session.commit()
if __name__ == '__main__':
    asyncio.run(main())

