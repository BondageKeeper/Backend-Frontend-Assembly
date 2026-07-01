async def create_order_info(order_data:EntireSchema,session: AsyncSession):
    validated_user_info = UserInfoDB(nickname=order_data.nickname,
                                     email=order_data.email,
                                     phone_number=order_data.phone_number,
                                     )
    session.add(validated_user_info)
    await session.flush()
    #for order in order_data.booking:
    from datetime import timedelta
    try:
        current_year = datetime.now().year
        complete_str = f'{order_data.arrival_time}.{current_year}'
        start_new_time = datetime.strptime(complete_str,'%d.%m %H:%M.%Y') #pattern in browser:  $Y-%m-%dT%H:%M
    except ValueError:
        raise HTTPException(status_code=400,detail="Invalid format / Please use DD.MM HH:MM")
    end_new_time = start_new_time + timedelta(hours=order_data.gaming_hours)
    time_request = select(TimeArrangementsDB).where(
        TimeArrangementsDB.computer_id == order_data.computer_id,
        TimeArrangementsDB.start_time < end_new_time,
        TimeArrangementsDB.end_time > start_new_time
    )
    found_result = await session.execute(time_request)
    overlapping_booking = found_result.scalar_one_or_none()
    if overlapping_booking is not None:
        raise HTTPException(status_code=400,detail=f'Computer #{order_data.computer_id} is already engaged during this time!')
    validated_order_booking = BookingInfoDB(
        computer_id = order_data.computer_id,
        gaming_hours = order_data.gaming_hours,
        additional_services = order_data.additional_services,
        arrival_time = start_new_time,
        user_id = validated_user_info.user_id
    )
    session.add(validated_order_booking)
    request_status = select(ComputersDB.id).where(ComputersDB.id == order_data.computer_id)
    result = await session.execute(request_status)
    computer_gotten_id = result.scalar_one_or_none()
    if not computer_gotten_id:
        raise HTTPException(status_code=404,detail='There is no such model')
    validated_time = TimeArrangementsDB(
                                        computer_id = computer_gotten_id,
                                        start_time = start_new_time,
                                        end_time = end_new_time
                                       )
    #validated_user_info.knot_booking.append(validated_order_booking)
    session.add(validated_time)
    #session.add(validated_user_info)
    await session.commit()
    #await session.refresh(validated_user_info, attribute_names=["knot_booking"])
    return {
        "status" : 201,
        "personal_id" : validated_user_info.user_id,
    }
