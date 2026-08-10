from fastapi import HTTPException , APIRouter , status , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Backend_password_page.app.crud_password_page import keep_open_database
from Backend_password_page.app.instance_password_page import TableFrameworkCO , TableSignInCO
from Backend_password_page.app import crud_password_page
from Backend_password_page.app.hashed_password import hash_password , verify_password

router = APIRouter(prefix='/password_page')

@router.post("/create_password",status_code=status.HTTP_201_CREATED)
async def create_password(instance: TableFrameworkCO,session: AsyncSession = Depends(keep_open_database)):
    user_dict = instance.model_dump()
    user_dict["password"] = hash_password(user_dict["password"])
    new_user = await crud_password_page.create_password(instance=TableFrameworkCO(**user_dict),session=session)
    return {"status":"success","user":user_dict["nickname"]}

@router.post("/sign-in")
async def sign_in(instance: TableSignInCO,session: AsyncSession = Depends(keep_open_database)):
     user_email = instance.email
     found_email = await crud_password_page.get_user_email(user_email,session)
     if found_email is None:
         raise HTTPException(status_code=404,detail="Email was not found!")
     else:
         written_parameters = instance.model_dump()
         if not verify_password(written_parameters["password"],found_email.password):
              raise HTTPException(status_code=401,detail="Wrong Password!")
         else:
             return {"status":"Welcome","user":found_email.nickname}


