from fastapi import HTTPException , APIRouter , status , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from PC_Bang.app.crud import keep_open_db
from PC_Bang.app.validation import  UserInfo
from PC_Bang.app import crud
router = APIRouter(prefix='/PC_BANG',tags=['Books'])

@router.get("/orders/{order_id}")
async def display_order_info(order_id: int,session: AsyncSession = Depends(keep_open_db)):
    order_info = await crud.get_order_info(order_id,session=session)
    if order_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='There are no any orders')
    return order_info

@router.post("/create_order",status_code=status.HTTP_201_CREATED)
async def create_order_info(given_data: UserInfo,session: AsyncSession = Depends(keep_open_db)):
    new_order = await crud.create_order_info(order_data=given_data,session=session)
    return new_order

@router.delete("/orders/{order_id}/cancel",status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order_info(order_id: int,session: AsyncSession = Depends(keep_open_db)):
    delete_info = await crud.delete_order_info(order_id,session=session)
    return delete_info
