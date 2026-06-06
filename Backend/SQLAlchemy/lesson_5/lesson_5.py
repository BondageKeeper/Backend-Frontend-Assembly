#if we just call func.avg() it will count and give us one number(average number) which was obtained from ALL data of users
#but what if we want to divide all users into groups and count avg value of each group(classified by name)
#in that case we use .group_by() - works like in SQL databases , an example:
from sqlalchemy import ForeignKey
from sqlalchemy import select , desc , asc , func
DATABASE_TRY_URL = 'postgresql+asyncpg://postgres:0631@127.0.0.1:5432/try707'
engine = create_async_engine(DATABASE_TRY_URL)
session = async_sessionmaker(engine, expire_on_commit=False)
class Base(DeclarativeBase):
    pass

class AIAgent(Base):
    __tablename__ = 'ai_agents'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()
    temperature: Mapped[float] = mapped_column()

class Users(Base):
    username: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("ai_agents.id"),ondelete="CASCADE")
    subscription: Mapped[str] = mapped_column('just imagine here Relationship synchronization flag - it is layout anyway')

async def get_avg_temp_per_user():
    async with session() as structure_data:
        query = (select(
            Users.username,
            func.avg(AIAgent.temperature).label('user_avg_temperature'),
            func.count(AIAgent.id).label('agents_count')
            ).join(AIAgent)
            .group_by(Users.username)
        )
        result = await structure_data.execute(query)
        for row in result.all():
            print(f'User: {row.username} | Agents: {row.agents_count} | Average temperature: {round(row.user_avg_temperature,2)}')

#but what if we need to filter outcome results in accordance of aggregation functions , for example 'python,give me those users
#whose average temperature more than 0.8" - or something like that , we cannot 'where' here because database count only
#after where: sequence look like this: 1)where(not calculated) -> 2)avg functions(calculated but as we can see filter where
#is located one step behind) - so in that case for immediate calculations of agg-funcs we use flag having()
async def get_high_temperature_users():
    async with session() as structure_data:
        query = (select(
            Users.username,
            func.avg(AIAgent.temperature).label('user_avg_temperature')
        )
        .join(Users)
        .group_by(Users.username)
        #so here we filter results of agg-functions simultaneously dut to this method 'having'
        .having(func.avg(AIAgent.temperature) > 0.8)
                 )
        result = await structure_data.execute(query)
        for row in result.all():
            print(f'User: {row.username} (Average temperature: {row.user_avg_temperature:.2f})')
#before that we studied relationships , but if we make select(Users) and get 100 users and after that in the loop for
#we start calling for each user user.subscription - SQLAlchemy will make 100 discrete , hidden requests in database
# - it will just simply kill our server
#if we want to prevent such a problem , we need to upload all these subscriptions of user(or other things) instantly
#saving them in db , flag 'selectinload' is used in this case , for instance:
from sqlalchemy.orm import selectinload
async def get_users_with_subscriptions_safely():
    async with session() as structure_data:
        query = (
            select(Users)
            #immediately we upload a list of subscriptions from database due to just one flag(server won't crash now)
            .options(selectinload(Users.subscription))
        )
        result = await structure_data.execute(query)
        users_list = result.scalars().all()
        for user in users_list:
            print(f'User: {user.username},amount of subscriptions: {len(user.subscription)}')

