# Проект py_dd

В проекте содержится приложение stocks, которое получает
данные с мосбиржи, сохраняет их в базу данных и отображает в html.
Работает в docker compose.

## Настройка

Установите docker.
Создайте файл **.env** в корне проекта рядом с файлом **.env.example**.
Инструкция по получению значения SECRET_KEY:
```
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```
Остальные значения придумываете сами.

## Запуск

Перейти в корень проекта и ввести:
docker compose -d --build
