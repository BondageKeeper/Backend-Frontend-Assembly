FROM python:3.11-slim
WORKDIR /backend_app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "Backend_planner.app.main_password_page:app", "--host", "0.0.0.0", "--port", "8443", "--ssl-keyfile", "/etc/letsencrypt/live/cards-hub.website/privkey.pem", "--ssl-certfile", "/etc/letsencrypt/live/cards-hub.website/fullchain.pem"]
