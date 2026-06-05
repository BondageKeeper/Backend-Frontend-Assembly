#There is 'smart select' where we can add:
#1)limit(5) - first five items / 2)order_by(desc) - to sort in order / 3).offset(0) - skip first 0 strings
from sqlalchemy import select , desc , asc
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
async def latest_prompts(key_role: int):
    async with session() as structure_data:
        query = (
            select(AIAgent).where(AIAgent.role == key_role)
            .order_by(desc(AIAgent.id)) #here we sort these chosen roles
            .limit(5) #here we take only five strings
            .offset(0) #here we skip 0 first items(strings)
        )
        result = await structure_data.execute(query)
        return result.scalars().all()

#also ofcourse we must know how to join tables(useful if we print values out from two tables) , here is an example:
class Users(Base):
    tokens: Mapped[int] = mapped_column(default=100)
async def get_requests_with_username():
    async with session() as structure_data:
        query = (
            select(AIAgent.name,Users.tokens).join(Users).where(AIAgent.role == 'vip')
        )#in join I wrote Users because Users is supposed to have Foreighkey(just let imagine that it has)
        result = await structure_data.execute(query)
        #we take specific columns so we just don't need scalars:
        for row in result.all():
            print(f"User tokens: {row.tokens} wrote prompt: {row.name}")

from sqlalchemy import func , select
async def get_agent_and_user_stats():
    async with session() as structure_data:
        query = (
            select(
                func.count(AIAgent.id).label('total_agents'),
                func.avg(AIAgent.temperature).label('average_temp'),
                func.sum(Users.tokens).label('all_users_tokens') #here we just sum all tokens of users
            ).join(Users)
        )
        result = await structure_data.execute(query)
        stats = result.one()
        print(f"Amount of agents on server: {stats.total_agents}")
        print(f"Average temperature of AI: {stats.average_temp:.2f}")
        print(f"Total amount of tokens: {stats.all_users_tokens}")

