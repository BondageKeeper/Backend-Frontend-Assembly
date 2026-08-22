from fastapi import HTTPException , APIRouter , status , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Backend_planner.app.crud_password_page import keep_open_database
from Backend_planner.app.instance_password_page import TableFrameworkCO , TableSignInCO , TableForgotPasswordCO , TableCreateCardsCO
from Backend_planner.app import crud_password_page
from Backend_planner.app.email_sender import send_recovery_email
from Backend_planner.app.hashed_password import hash_password , verify_password
from faker import Faker
fake = Faker('en_US')

router = APIRouter(prefix='/password_page')

@router.post("/create_password",status_code=status.HTTP_201_CREATED)
async def create_password(instance: TableFrameworkCO,session: AsyncSession = Depends(keep_open_database)):
    user_dict = instance.model_dump()
    user_dict["password"] = hash_password(user_dict["password"])
    new_user = await crud_password_page.create_password(instance=TableFrameworkCO(**user_dict),session=session)
    return {"status_code": 200,"user": f'Welcome, {user_dict["nickname"]}!'}

@router.post("/sign-in")
async def sign_in(instance: TableSignInCO,session: AsyncSession = Depends(keep_open_database)):
     user_email = instance.email
     found_email = await crud_password_page.get_user_email(user_email,session)
     if found_email is None:
         raise HTTPException(status_code=404,detail=": Email was not found!")
     else:
         written_parameters = instance.model_dump()
         if not verify_password(written_parameters["password"],found_email.password):
              raise HTTPException(status_code=401,detail=": Wrong Password!")
         else:
             return {
                 "status_code" : 200,
                 "nickname" : found_email.nickname
             }

@router.post("/forgot_password")
async def forgot_password(instance: TableForgotPasswordCO,session: AsyncSession = Depends(keep_open_database)):
    user_email = instance.email
    found_email = await crud_password_page.get_user_email(user_email,session)
    if found_email is None:
        raise HTTPException(status_code=404, detail=": Email was not found!")
    else:
        new_password = fake.bothify(text='??????????#####')
        new_hashed_password = hash_password(new_password)
        await crud_password_page.update_user_password(
            nickname = found_email.nickname,
            new_hash = new_hashed_password,
            session = session
        )
    email_sending = send_recovery_email(receiver_email=found_email.email,new_password=new_password)
    if not email_sending:
        raise HTTPException(status_code=500,detail="Failed to send email. Try again later.....")
    else:
        return {
            'status_code' : 200,
            'comment' : 'new password has been sent to your email!'
        }

@router.post("/save_cards")
async def save_cards(instance: TableCreateCardsCO,session: AsyncSession = Depends(keep_open_database)):
    await crud_password_page.store_cards(instance=instance,session=session)
    return {"status_code" : 200}

