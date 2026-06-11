from fastapi import FastAPI , Depends , HTTPException , status
from pydantic import BaseModel , Field
from sqlalchemy.orm import mapped_column , Mapped , DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker , create_async_engine , AsyncSession
import asyncio

class Base(DeclarativeBase):
    pass

class AILog(Base):
    __tablename__ = 'cool_code228'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int]
    prompt_text: Mapped[str]
    ai_response: Mapped[str]

class Validation(BaseModel):
    user_id: int
    prompt_text: str = Field(min_length=10,max_length=100)
    ai_response: str = Field(default='UNKNOWN')

app = FastAPI()
DATABASE_URL = 'postgresql+asyncpg://postgres:0631@127.0.0.1:5432/cool_code228'
engine = create_async_engine(DATABASE_URL)
engine_session = async_sessionmaker(engine,expire_on_commit=False)

async def get_db():
    async with engine_session() as session:
        yield session

@app.post("/api/predict",status_code=status.HTTP_201_CREATED)
async def predict_and_log(
        given_data: Validation,
        session: AsyncSession = Depends(get_db)):
    if given_data.user_id == 666:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is banned")
    fake_response = f'AI response for {given_data.prompt_text[:20]}...'
    validated_logs = AILog(
        user_id=given_data.user_id,
        prompt_text=given_data.prompt_text,
        ai_response=fake_response
    )
    """Here we save result in db:"""
    session.add(validated_logs)
    await session.commit()
    await session.refresh(validated_logs)
    return { #this answer will be addressed to the user
        "status": "success",
        "log_id": validated_logs.id,
        "ai_response": fake_response

    }

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())

