FROM python:3.11-slim
WORKDIR /backend_app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn","PC_Bang.app.main:app","--host","0.0.0.0","--port","8080"]
