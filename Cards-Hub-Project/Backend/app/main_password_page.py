from fastapi import FastAPI , Request , status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from Backend_planner.app.routers import all_methods
from Backend_planner.app.crud_password_page import engine_origin , AlchemyLaunch
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
import os
@app.get('/')
async def root():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    html_path = os.path.join(base_dir, 'Frontend_password_page', 'html_page.html')
    return FileResponse(html_path)

@app.on_event("startup")
async def launch_server():
    async with engine_origin.begin() as loading:
        await loading.run_sync(AlchemyLaunch.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run(
        "Backend_planner.app.main_password_page:app",
        host="0.0.0.0",
        port=8443,  #port of security traffic
        ssl_keyfile="/etc/letsencrypt/live/cards-hub.website/privkey.pem",
        ssl_certfile="/etc/letsencrypt/live/cards-hub.website/fullchain.pem"
    )



