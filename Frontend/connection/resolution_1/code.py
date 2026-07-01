logger.add('Users_registration_errors.log',rotation='300 MB',retention=5,level='INFO')
app = FastAPI(title='CyberClub API')
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex = r".*",
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
app.include_router(booking_storage.router)

@app.get('/')
async def root():
    return {"message" : "Write docs in the route please..."}
