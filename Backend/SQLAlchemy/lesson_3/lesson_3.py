#now , let's try to combine pydantic with learned sql methods - this is just an example(so-called layout)
import asyncio
from pydantic import BaseModel , Field , field_validator
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker , create_async_engine
from loguru import logger
#at the beginning we write pydantic(validation) layer
class AgentCreateSchema(BaseModel):
    agent_name: str = Field(min_length=3,max_length=20)
    role: str
    temperature: float = Field(default=0.7,ge=0.0,le=2.0)
    @field_validator("agent_name")
    @classmethod
    def check_name(cls,value:str):
        import re
        if re.findall(r'scam',value,flags=re.IGNORECASE):
            raise ValueError('This name of agent is prohibited')
        return value
#after that we make a database using sqlalchemy
class Base(DeclarativeBase):
    pass

class AIAgent(Base):
    __tablename__ = 'ai_agents'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()
    temperature: Mapped[float] = mapped_column()
DATABASE_TRY_URL = 'postgresql+asyncpg://postgres:0631@127.0.0.1:5432/try707'
engine = create_async_engine(DATABASE_TRY_URL)
session = async_sessionmaker(engine, expire_on_commit=False)
async def process_user_input(raw_data: dict):
    #if data doesn't satisfy validation than we raise error:
    validated_data = AgentCreateSchema(**raw_data)
    logger.info('Data is suitable!')
    #here we create well_validated class which already will be DeclarativeBase class
    new_agent = AIAgent(
        name = validated_data.agent_name,
        role = validated_data.role,
        temperature = validated_data.temperature
    )
    async with engine.begin() as structure_preparation:
        await structure_preparation.run_sync(Base.metadata.create_all)
    async with session() as engine_session:
        engine_session.add_all([new_agent])
        await engine_session.commit()
if __name__ == '__main__':
    try:
        asyncio.run(process_user_input({
            "agent_name" :  "Pro-ScAm",
            "role" : "Writing Clean Python Code",
            "temperature" : 0.5
        }))
    except Exception as error:
        logger.warning(f'Structure was violated! {error}')

