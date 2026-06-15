"""Structure of the site project:"""
#1 BACKEND/app:
#a) main.py(here we create so-called entrance and also launch FastAPI
#b) database.py(here we create a connection to the database)
#2 BACKEND/app/routers (what Swagger sees) - endpoints
#a) __init.py
#b) orders.py (logic of orders or other things)
#3 BACKEND/app
#a) schemas.py (pydantic models for validation)
#b) crud.py (functions for working with database)
#4 BACKEND/requirements.txt
#FRONTEND/index.html (this is for a main page of a future site)
