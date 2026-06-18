from PC_Bang.app.routers import booking_storage
from PC_Bang.app.crud import engine , AlchemyLaunch
from loguru import logger
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
logger.add('Users_registration_errors.log',rotation='300 MB',retention=5,level='INFO')
app = FastAPI(title='CyberClub API')
app.include_router(booking_storage.router)

@app.get('/')
async def root():
    return {"message" : "Write docs in the route please..."}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,exc: RequestValidationError):
    error_details = exc.errors()
    logger.error(f'Validation failed for URL {request.url}.Errors: {error_details}')
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_details}
    )

@app.on_event("startup")
async def start_server_task():
    async with engine.begin() as loading:
        await loading.run_sync(AlchemyLaunch.metadata.create_all)
if __name__ == "__main__":
    uvicorn.run("PC_Bang.app.main:app",host="127.0.0.1",port=8080,reload=True)
