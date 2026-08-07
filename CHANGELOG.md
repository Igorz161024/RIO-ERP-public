# CHANGELOG

## [2026-08-03] — Перехід до нового фронтенду
- Додано директорію `frontend_rio` для RIO-фронтенду
- Оновлено `docker-compose.yml`: прибрано React-фронт, залишено бекенд + БД + nginx + backup
- Налаштовано окрему мережу `erp_network` для нового проєкту
- Підтверджено паралельну роботу двох проєктів (Diplom-project та RIO-ERP)
- Підготовлено базову структуру для інтеграції RIO-фронтенду

## [2026-07-30] — Тестування бекенду
- Запуск FastAPI-бекенду у двох контейнерах (`erp_backend1`, `erp_backend2`)
- Перевірка підключення до бази `erp_diplom`
- Swagger-інтерфейс доступний на `http://localhost:8000/docs`

## [2026-07-25] — Ініціалізація RIO-ERP
- Створено новий репозиторій
- Додано базову конфігурацію Docker
- Піднято контейнер PostgreSQL (`erp_db`)
## [2026-08-05] Added RIO-ERP project structure

### Added
- Створено базову структуру бекенду (backend/):
  - routers для Finance, Inventory, Sales, Purchases, Legal
  - базові модулі (auth.py, database.py, schemas/)
  - Dockerfile та requirements.txt
- Створено структуру фронтенду (frontend_rio/):
  - services для Finance, Inventory, Journal, Legal, Purchases, Sales, Users
  - ui-сторінки для кожного модуля
  - main.py з реєстрацією сторінок
  - rio.toml для конфігурації
- Додано docker-compose.yml для інтеграції бекенду та фронтенду
- Додано README.md, LICENSE, CHANGELOG.md

### Changed
- Налаштовано стабільний порт для фронтенду Rio: 9000
- Оновлено конфігурацію запуску через `rio run --port 9000`

### Notes
- API ще не реалізовані, фронтенд наразі показує пусті сторінки.
- Наступний крок: інтеграція тестових даних у UI для перевірки відображення.
## [1.0.0] - 07.08.2026
### Added
- Реалізовано повний набір CRUD‑роутерів для Accounts, Journal, Finance, Legal, Sales, Inventory, Purchases.
- Додано Pydantic‑схеми (Create, Update, Schema) для всіх сутностей.
- Підключено Swagger UI з автоматичною генерацією OpenAPI 3.1.
- Запуск бекенду FastAPI на порту 7000 (RIO‑ERP backend).
- Фінансовий модуль розширено ендпоінтами: balance, add_entry, report, plot.
