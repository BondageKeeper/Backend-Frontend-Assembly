from pydantic import BaseModel , Field , field_validator , EmailStr

class BookingInfo(BaseModel):
    computer_id: int
    gaming_hours: int
    additional_services: bool
    arrival_time: str = Field(examples=['24.06 18:30'])

class UserInfo(BaseModel):
    nickname: str = Field(min_length=2,max_length=15)
    email: EmailStr
    phone_number: str = Field(min_length=11,max_length=12)
    booking: list[BookingInfo]
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
