from fastapi import HTTPException , APIRouter , status , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Backend_password_page.app.crud_password_page import keep_open_database
from Backend_password_page.app.instance_password_page import TableFrameworkCO , PresentCredentials
from Backend_password_page.app import crud_password_page
router = APIRouter(prefix='/password_page')

@router.post("/create_password",status_code=status.HTTP_201_CREATED)
async def create_password(instance: TableFrameworkCO,session: AsyncSession = Depends(keep_open_database)):
    new_password = await crud_password_page.create_password(instance=instance,session=session)
    return new_password

@router.post("/return_to_account",status_code=status.HTTP_201_CREATED)
async def return_to_account(instance: PresentCredentials,session: AsyncSession = Depends(keep_open_database)):
    checking = await crud_password_page.return_to_account(instance=instance,session=session)



