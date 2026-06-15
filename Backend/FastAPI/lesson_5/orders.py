#backend/api/routers/orders.py (here we deal with our FastAPI samples
from fastapi import HTTPException , APIRouter
from app import schemas , crud
#here we create isolated router for our orders:
router = APIRouter(prefix="/orders",tags=["Orders"])
@router.get("/{order_id}",response_model=schemas.OrderResponse)
def get_order_status(order_id: int):
    #router simply calls function from crud.py
    order = crud.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404,detail='Order is not found')
    return order
