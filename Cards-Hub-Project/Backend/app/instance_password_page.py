from pydantic import BaseModel , Field , field_validator
from fastapi import status

class TableFrameworkCO(BaseModel):
    nickname: str = Field(min_length=2,max_length=20)
    email: str
    password: str
    @field_validator("email")
    @classmethod
    def check_domen(cls,email: str):
        import re
        if not re.findall(r'[\w\-.]+@(?:gmail\.com|yandex\.ru)',email):
            raise ValueError('Please , use yandex.ru or gmail.com domens!')
        return email

class TableSignInCO(BaseModel):
    email: str
    password: str
    @field_validator("email")
    @classmethod
    def check_domen(cls,email: str):
        import re
        if not re.findall(r'[\w\-.]+@(?:gmail\.com|yandex\.ru)',email):
            raise ValueError('Please , use yandex.ru or gmail.com domens!')
        return email

class TableForgotPasswordCO(BaseModel):
    email: str
    @field_validator("email")
    @classmethod
    def check_domen(cls,email: str):
        import re
        if not re.findall(r'[\w\-.]+@(?:gmail\.com|yandex\.ru)',email):
            raise ValueError('Please , use yandex.ru or gmail.com domens!')
        return email

class TableCreateCardsCO(BaseModel):
    user_email: str
    todo_column: list
    progress_column: list
    done_column: list

