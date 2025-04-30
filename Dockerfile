# Указываем базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями и устанавливаем их
COPY pyproject.toml ./
COPY poetry.lock ./.


RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
