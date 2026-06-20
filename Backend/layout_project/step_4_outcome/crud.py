from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker , AsyncSession
from sqlalchemy.orm import relationship , Mapped , mapped_column , DeclarativeBase
from datetime import datetime
from PC_Bang.app.validation import UserInfo

class AlchemyLaunch(DeclarativeBase):
    pass

class TimeArrangementsDB(AlchemyLaunch):
    __tablename__ = 'time_tables'
    id: Mapped[int] = mapped_column(primary_key=True)
    computer_id: Mapped[int] = mapped_column(ForeignKey('club_computers.id',ondelete='CASCADE'))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    knot_computer: Mapped['ComputersDB'] = relationship(back_populates='knot_time_arrangements')

class ComputersDB(AlchemyLaunch):
    __tablename__ = 'club_computers'
    id: Mapped[int] = mapped_column(primary_key=True)
    model_name: Mapped[str] = mapped_column(unique=True)
    knot_booking: Mapped[list['BookingInfoDB']] = relationship(back_populates='knot_computer')
    knot_time_arrangements: Mapped[list['TimeArrangementsDB']] = relationship(back_populates='knot_computer')

class BookingInfoDB(AlchemyLaunch):
    __tablename__ = 'booking_info'
    id: Mapped[int] = mapped_column(primary_key=True)
    computer_id: Mapped[int] = mapped_column(ForeignKey('club_computers.id'))
    gaming_hours: Mapped[int]
    additional_services: Mapped[bool]
    arrival_time: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey('users_info_registration.user_id',ondelete='CASCADE'))
    knot_user: Mapped['UserInfoDB'] = relationship(back_populates='knot_booking')
    knot_computer: Mapped['ComputersDB'] = relationship(back_populates='knot_booking')

class UserInfoDB(AlchemyLaunch):
    __tablename__ = 'users_info_registration'
    user_id: Mapped[int] = mapped_column(primary_key=True,unique=True)
    nickname: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[str]
    register_time: Mapped[datetime] = mapped_column(default=datetime.now())
    knot_booking: Mapped[list['BookingInfoDB']] = relationship(back_populates='knot_user')

DATABASE_URL = 'postgresql+asyncpg://postgres:0631@127.0.0.1:5432/PC_customers_v23'
engine = create_async_engine(DATABASE_URL,echo=True)
engine_session = async_sessionmaker(engine,expire_on_commit=False)

async def keep_open_db():
    async with engine_session() as session:
        yield session

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
async def get_order_info(order_id: int,session:AsyncSession):
    request = select(BookingInfoDB).where(BookingInfoDB.id == order_id).options(selectinload(BookingInfoDB.knot_user),
                                                                                selectinload(BookingInfoDB.knot_computer))
    result = await session.execute(request)
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404,detail='Booking was not found!')
    return {
        "status" : "success",
        "nickname" : order.knot_user.nickname,
        "order_id" : order.id,
        "computer_model" : order.knot_computer.model_name,
        "gaming_hours" : order.gaming_hours,
        "additional_services" : order.additional_services,
        "arrival_time" : order.arrival_time
    }

from sqlalchemy import update
async def create_order_info(order_data: UserInfo,session: AsyncSession):
    validated_user_info = UserInfoDB(nickname=order_data.nickname,
                                     email=order_data.email,
                                     phone_number=order_data.phone_number,
                                     )
    for order in order_data.booking:
        from datetime import timedelta
        try:
            current_year = datetime.now().year
            complete_str = f'{order.arrival_time}.{current_year}'
            start_new_time = datetime.strptime(complete_str,'%d.%m %H:%M.%Y')
        except ValueError:
            raise HTTPException(status_code=400,detail="Invalid format / Please use DD.MM HH:MM")
        end_new_time = start_new_time + timedelta(hours=order.gaming_hours)
        time_request = select(TimeArrangementsDB).where(
            TimeArrangementsDB.computer_id == order.computer_id,
            TimeArrangementsDB.start_time < end_new_time,
            TimeArrangementsDB.end_time > start_new_time
        )
        found_result = await session.execute(time_request)
        overlapping_booking = found_result.scalar_one_or_none()
        if overlapping_booking is not None:
            raise HTTPException(status_code=400,detail=f'Computer #{order.computer_id} is already engaged during this time!')

        validated_order_booking = BookingInfoDB(
            computer_id=order.computer_id,
            gaming_hours=order.gaming_hours,
            additional_services=order.additional_services,
            arrival_time= start_new_time
        )

        request_status = select(ComputersDB.id).where(ComputersDB.id == order.computer_id)
        result = await session.execute(request_status)
        computer_gotten_id = result.scalar_one_or_none()
        if not computer_gotten_id:
            raise HTTPException(status_code=404,detail='There is no such model')
        #request_update_status = update(ComputersDB).where(ComputersDB.id == computer_gotten_id).values(status='booked')
        #await session.execute(request_update_status)
        validated_time = TimeArrangementsDB(
                                            computer_id = computer_gotten_id,
                                            start_time = start_new_time,
                                            end_time = end_new_time
                                           )
        validated_user_info.knot_booking.append(validated_order_booking)
        session.add(validated_time)
    session.add(validated_user_info)
    await session.commit()
    await session.refresh(validated_user_info, attribute_names=["knot_booking"])
    return {
        "status" : 201,
        "personal_id" : validated_user_info.user_id,
        "order_id" : [booking.id for booking in validated_user_info.knot_booking]
    }

from sqlalchemy import delete
async def delete_order_info(order_id: int,session: AsyncSession):
    request = select(BookingInfoDB).where(BookingInfoDB.id == order_id).options(selectinload(BookingInfoDB.knot_user))
    result = await session.execute(request)
    deleted_order = result.scalar_one_or_none()
    user_to_delete = deleted_order.knot_user
    arrangement_to_delete = delete(TimeArrangementsDB).where(
        TimeArrangementsDB.computer_id == deleted_order.computer_id,
                    TimeArrangementsDB.start_time == deleted_order.arrival_time
                                                            )
    if deleted_order is None:
        raise HTTPException(status_code=404,detail='Booking was not found!')
    else:
        await session.execute(arrangement_to_delete)
        await session.delete(deleted_order)
        await session.delete(user_to_delete)
        await session.commit()
        return {
            "status" : "booking was deleted successfully!"
        }

from datetime import timedelta
import zoneinfo
async def check_models_states(session: AsyncSession):
    result_states_list = []
    request = select(ComputersDB).options(selectinload(ComputersDB.knot_time_arrangements))
    result = await session.execute(request)
    all_computers_info = result.scalars().all()
    for one_computer in all_computers_info:
        current_time = datetime.now(zoneinfo.ZoneInfo("Europe/Moscow")).replace(tzinfo=None)
        for arrangement in one_computer.knot_time_arrangements:
            if arrangement.start_time <= current_time <= arrangement.end_time:
                result_states_list.append({
                    "computer_id": one_computer.id, "model_name": one_computer.model_name, "status": "busy"
                })
            else:
                result_states_list.append({
                    "computer_id": one_computer.id, "model_name": one_computer.model_name, "status": "free"
                })
    return result_states_list

from sqlalchemy import func , select , desc
async def count_revenue_info(session: AsyncSession):
    request = (select(
        func.sum(BookingInfoDB.gaming_hours).label('total_hours'),
        func.count(UserInfoDB.user_id).label('total_customers')
    ).join(UserInfoDB))
    result = await session.execute(request)
    total_value = result.fetchone()
    return {
          'total_revenue' : float(total_value.total_hours or 0) * 150.0,
          'customers_amount' : int(total_value.total_customers)
    }

async def count_popular_models(session: AsyncSession):
    request = (select(
        ComputersDB.model_name,
        func.count(BookingInfoDB.id).label('computers_popularity')
    ).join(BookingInfoDB).group_by(ComputersDB.model_name).order_by(func.count(BookingInfoDB.id).desc()))
    result = await session.execute(request)
    total_value = result.all()
    return [
        {"model_name" : row.model_name,
         "popularity" : row.computers_popularity}
    for row in total_value ]
