from fastapi import FastAPI , Request , status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from Backend.app.routers import all_methods
from Backend.app.crud_password_page import engine_origin , AlchemyLaunch
from fastapi.responses import FileResponse

app = FastAPI(title='Password Page')
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex = r".*",
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
app.include_router(all_methods.router)
@app.get('/')
async def root():
    return {'There is nothing here , write docs pleasee...'}
     

@app.on_event("startup")
async def launch_server():
    async with engine_origin.begin() as loading:
        await loading.run_sync(AlchemyLaunch.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run("Backend.app.main_password_page:app",host="127.0.0.1",port=8080,reload=True)
