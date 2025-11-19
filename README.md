# Library Management System

REST API для системы управления библиотекой на Python с FastAPI.

## Структура проекта

- `models/` - Сущности базы данных
- `schemas/` - DTO объекты
- `repositories/` - Доступ к данным
- `services/` - Бизнес-логика
- `controllers/` - REST API endpoints
- `config/` - Конфигурация приложения

## Запуск проекта

1. Установите зависимости:
```bash
pip install -r requirements.txt
```
2. Настройте базу данных в config/database.py
3. 
- Установите MySQL Server;
- Создайте базу данных: CREATE DATABASE library_db;
- Настройте подключение в config/database.py;
4. Запустите приложение:
```bash
python main.py
```
5. Откройте документацию API: 
Swagger UI: http://localhost:8000/docs - для тестирования
ReDoc: http://localhost:8000/redoc


