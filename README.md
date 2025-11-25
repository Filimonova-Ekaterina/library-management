# Library Management System

REST API для системы управления библиотекой на Python с FastAPI.

## Структура проекта

- `models/` - Сущности базы данных
- `schemas/` - DTO объекты
- `repositories/` - Доступ к данным
- `services/` - Бизнес-логика
- `controllers/` - REST API endpoints
- `config/` - Конфигурация приложения
- `tests/` - Тестирование приложения

## Запуск проекта

1. Клонируйте репозиторий
```bash
git clone https://github.com/Filimonova-Ekaterina/library-management.git
```
2. Перейдите в директорию проекта
```bash
cd library-management
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Настройте базу данных в config/database.py
5. 
- Установите MySQL Server;
- Создайте базу данных: CREATE DATABASE library_db;
- Настройте подключение в config/database.py;
6. Запустите приложение:
```bash
python main.py
```
Или с помощью uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
7. Откройте документацию API: 
Swagger UI: http://localhost:8000/docs - для тестирования
ReDoc: http://localhost:8000/redoc

## Запуск тестов
#Быстрая команда для всех тестов
```bash
pytest
```
#Только unit тесты
```bash
python -m pytest tests/unit/ -v
```
#Только integration тесты
```bash
python -m pytest tests/integration/ -v
```



