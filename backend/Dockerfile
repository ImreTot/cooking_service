FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
COPY .env .
CMD ["python", "manage.py", "runserver", "0:8000"]