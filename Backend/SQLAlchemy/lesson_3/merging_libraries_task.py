from loguru import logger
from pydantic import Field , field_validator , BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship , Mapped , mapped_column , DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker , create_async_engine
import asyncio
from faker import Faker
fake = Faker('en_US')

DATABASE_URL = 'postgresql+asyncpg://postgres:0631@127.0.0.1:5432/merge01'
engine = create_async_engine(DATABASE_URL)
engine_session = async_sessionmaker(engine,expire_on_commit=False)

class MainBranchAlchemy(DeclarativeBase):
    pass

class Users(MainBranchAlchemy):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    github_url: Mapped[str] = mapped_column()
    '''Relationship synchronization flag'''
    subscription: Mapped[list['Subscriptions']] = relationship(back_populates='user')

class Subscriptions(MainBranchAlchemy):
    __tablename__ = 'users_subscriptions'
    id: Mapped[int] = mapped_column(primary_key=True)
    plan_name: Mapped[str]
    price: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    '''Relationship synchronization flag'''
    user: Mapped['Users'] = relationship(back_populates='subscription')

class ValidateUser(BaseModel):
    username: str = Field(min_length=1,max_length=15)
    github_url: str
    @field_validator("github_url")
    @classmethod
    def validate_github_path(cls,value: str):
        import re
        if not re.findall(r'https://github\.com/[a-zA-Z0-9-_]+',value):
            raise ValueError('Github is not found!')
        elif len(value.strip(' ')) == 0:
            raise ValueError('Write your github!')
        return value

class ValidateSubscriptions(BaseModel):
    plan_name: str = Field(min_length=3,max_length=10)
    price: int = Field(ge=0)
    @field_validator("plan_name")
    @classmethod
    def validate_plan_name(cls,value: str):
        import re
        if not re.findall(r'^(Free|Pro|Enterprise)$',value,flags=re.IGNORECASE):
            raise ValueError('Name of subscription is unknown!')
        return value

async def merge_alchemy_and_pydantic(sub_data: dict, user_data: dict):
    validated_data = ValidateSubscriptions(**sub_data)
    logger.info('loading...')
    validated_subscription = Subscriptions(
        plan_name = validated_data.plan_name,
        price = validated_data.price
    )
    validated_user_data = ValidateUser(**user_data)
    validated_user = Users(
        username = validated_user_data.username,
        github_url = validated_user_data.github_url
    )
    validated_user.subscription.append(validated_subscription)
    async with engine.begin() as structure:
        await structure.run_sync(MainBranchAlchemy.metadata.create_all)
    async with engine_session() as session:
        session.add_all([validated_user])
        await session.commit()

if __name__ == '__main__':
    try:
        asyncio.run(merge_alchemy_and_pydantic(
            {
            'plan_name' : 'Free',
            'price' : '0.0'} ,

            {
            'username' : 'Ms.Trousers',
            'github_url' : 'https://github.com/cool_projects'
            }
        ))
    except Exception as error:
        logger.warning(f'Damn! There are some issues: {error}')


