FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH="/.venv" \
    APP_HOME="/app" \
    FLASK_APP="main.py"

WORKDIR $APP_HOME

COPY . .

# RUN python3 -m venv $VENV_PATH && \
#     $VENV_PATH/bin/pip install --upgrade pip && \
#     $VENV_PATH/bin/pip install -r requirements.txt


RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5000

CMD ["sh", "-c", "flask run --host=0.0.0.0"]
