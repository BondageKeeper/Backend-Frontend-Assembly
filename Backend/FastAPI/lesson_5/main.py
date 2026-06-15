#this file just gathers everything together:
from fastapi import FastAPI
from app.routers import orders
app = FastAPI(title='server of API delivery')
#after that we register our router in main application:
app.include_router(orders.router)
@app.get('/')
def root():
    return {"message":"backend works"}
