FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH="/.venv" \
    APP_HOME="/app" \
    FLASK_APP="main.py" 

WORKDIR $APP_HOME

COPY . .



RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN rm -f ./app/application/instance

EXPOSE 8080

# CMD ["sh", "-c", "flask run --host=0.0.0.0"]

CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
