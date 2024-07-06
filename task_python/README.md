## Стэк
    - Python
    - Poetry
    - FastAPI
    - SQLAlchemy
    - Alembic
    - PostgreSQL
    - Uvicorn
    - Asynio

## Установка зависимостей
    - pip install poetry
    - poetry install

## Без Docker
    - sudo docker-compose up -d postgres_services
    - alembic upgrade head
    - uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

## C Docker
    - sudo docker-compose up