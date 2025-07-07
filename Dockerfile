
# Используем официальный python-образ как базовый
FROM python:3.11-slim

# Устанавливаем сборочные зависимости (libpq-dev не нужен для SQLite!)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Задаём рабочую директорию внутри контейнера
WORKDIR /app

# Копируем только файл зависимостей для более эффективного кэширования
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем остальной проект в контейнер
COPY . .

# (По желанию) Собрать статические файлы Django сразу при билде
# RUN python manage.py collectstatic --noinput

# Открываем порт 8000 для приложения
EXPOSE 8000

# Запускаем gunicorn (замени 'mailsender' на имя своего проекта, если оно изменишь!)
CMD ["gunicorn", "mailsender.wsgi:application", "--bind", "0.0.0.0:8000"]
