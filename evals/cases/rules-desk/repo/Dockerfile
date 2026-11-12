FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn
COPY . .
CMD ["sh", "-c", "python deskctl.py migrate && gunicorn -b 0.0.0.0:8080 desk.app:app"]
