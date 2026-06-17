from fastapi import FastAPI
import uvicorn
from PC_Bang.app.routers import booking_storage
app = FastAPI(title='CyberClub API')
app.include_router(booking_storage.router)
@app.get('/')
async def root():
    return {"message" : "Write docs in the route please..."}
if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8080,reload=True)
