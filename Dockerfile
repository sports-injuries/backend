FROM python:3.11-slim

WORKDIR /app

# install requirements
COPY requirements.txt /app/
RUN python -m pip install -r requirements.txt

COPY backend /app/backend

CMD [ "python", "-m", "backend" ]
