from pydantic import BaseModel , Field , field_validator , EmailStr
from datetime import datetime
from loguru import logger

class BookingInfo(BaseModel):
    id: int
    computer_model: str
    gaming_hours: str
    additional_services: bool
    arrival_time: datetime

class UserInfo(BaseModel):
    user_id: int
    nickname: str = Field(min_length=2,max_length=15)
    email: EmailStr
    phone_number: str = Field(min_length=12)
    register_time: datetime
    booking: list[BookingInfo]
    logger.add('Users_registration_errors.log',rotation='300 MB',retention=5,level='INFO')
    @field_validator('phone_number')
    @classmethod
    def phone_number_validation(cls,phone_number: str):
        import re
        if not re.findall(r'^(\+?7|8)\d{10}$',phone_number):
            raise ValueError('User has invalid phone number!')
        return phone_number
    @field_validator('nickname')
    @classmethod
    def name_validation(cls,nickname: str):
        import re
        if re.findall('(bot|scam|lottery|casino|ai|robot|system)',nickname,flags=re.IGNORECASE):
            raise ValueError('The prohibited name is found!')
        return nickname
