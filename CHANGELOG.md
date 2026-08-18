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
## [1.0.0] — 07.08.2026
### Added
- Реалізовано повний набір CRUD‑роутерів для Accounts, Journal, Finance, Legal, Sales, Inventory, Purchases.
- Додано Pydantic‑схеми (Create, Update, Schema) для всіх сутностей.
- Підключено Swagger UI з автоматичною генерацією OpenAPI 3.1.
- Запуск бекенду FastAPI на порту 7000 (RIO‑ERP backend).
- Фінансовий модуль розширено ендпоінтами: balance, add_entry, report, plot.
- Додано Dockerfile та requirements для бекенду й фронтенду RIO.

### Changed
- Оновлено структуру директорій backend/ та frontend_rio/.
- Видалено застарілий файл `journal_window.py` у фронтенді.
- Перенесено логіку у модулі та роутери з чітким розділенням схем і моделей.

### Fixed
- Виправлено імпорти у `schemas/__init__.py` (додано accounts).
- Усунено конфлікт портів: бекенд працює на 7000, фронтенд RIO‑ERP на 9000, React на 8000.
## [2026-08-12] Оновлення структури бекенду
- Додано нову модель `user.py` у backend/models
- Додано відповідну схему `user.py` у backend/schemas
- Додано роутер `users_router.py` у backend/routers
- Переміщено `database.py` у корінь backend/
- Видалено зайві файли з директорій models та schemas
- Структура директорій очищена: залишилися тільки ORM‑класи, Pydantic‑схеми та роутери
- Переписано код із тестового варіанту на продакшн‑реалізацію (оновлені моделі, схеми та роутери)
- Модуль Accounts переписано на ORM:
  • створено модель Account з двостороннім зв’язком із Journal
  • додано Pydantic‑схеми (AccountBase, AccountCreate, AccountUpdate, AccountSchema) з підтримкою orm_mode
  • реалізовано CRUD‑роутер (accounts_router.py) із перевіркою токена (get_current_user) та роботою через ORM‑сесію
  • видалено залишки тестових заглушок (fake_db)
## [2026-08-13] Init schema migration

### Основні зміни
- Створено початкову міграцію `init schema` для бази даних `erp_diplom`.
- Міграція успішно застосована (`alembic upgrade head`).
- У PostgreSQL створено актуальну структуру таблиць:
  - `accounts`
  - `journal`
  - `finance`
  - `inventory`
  - `purchases`
  - `sales`
  - `legal`

### Деталі реалізації
- Додано файл `backend/database.py` з оголошенням `Base = declarative_base()`.
- Виправлено імпорти у моделях: тепер усі класи наслідують від `Base` з `backend.database`.
- У моделі `Journal` додано зовнішній ключ `account_id` та двосторонній зв’язок із `Account`.
- У моделі `Account` додано `journals = relationship("Journal", back_populates="account")`.
- Виправлено імпорти у `env.py` (тепер використовуються правильні назви файлів: `accounts`, `purchase`, `sale`).
- Виправлено помилки у `__init__.py` для моделей (невідповідність назв класів у множині/однині).
- Alembic тепер коректно бачить усі моделі через `target_metadata = Base.metadata`.

### Результат
- Схема бази даних синхронізована з моделями.
- Автоматично згенеровано файл міграції:  
  `backend/alembic/versions/fc35bc4a14d0_init_schema.py`
- ERP‑проєкт готовий до подальших змін через нові міграції.
### 15.08.2026
- Оновлено main.py: додано генерацію JWT токена з полем role, виправлено get_current_user для перевірки username + role.
- Додано Pydantic‑схеми AccountSchema та JournalSchema для коректної серіалізації ORM‑об’єктів у JSON.
- Переписано ендпоінти /api/accounts/ та /api/journal/ з response_model, щоб уникнути Internal Server Error.
- Налаштовано роботу з токеном у PowerShell: збереження у змінну $TOKEN та використання у заголовках Authorization.
- Перезапущено контейнери rio_backend1, rio_backend2, rio_erp_db — статус Healthy, бекенди стартують стабільно.
- Проведено тестові виклики API, зафіксовано проблему з Invalid token, визначено наступний крок — перевірка CRUD після оновлення main.py.
## 2026-08-18

### Frontend
- Переписано main.py для запуску як постійного FastAPI‑сервера
- Додано кореневий маршрут `/` з повідомленням про роботу фронтенду
- Реалізовано проксі‑маршрути `/finance` та `/sales` для інтеграції з бекендами
- Збережено RIO‑UI меню та сторінки (journal, finance, inventory, sales, purchases, legal, users)
- Контейнер `rio_frontend` тепер стабільно працює на порту 3001

### Backend
- Переписано main.py для стабільного запуску через Uvicorn
- Додано постійний серверний режим (FastAPI) замість одноразового виконання
- Розширено main.py для підтримки всіх модулів (accounts, journal, entry_lines, finance, inventory, sales, purchases, legal, users)
- Виправлено завершення процесу після старту — тепер бекенд працює без зупинки
- Підтримка інтеграції з фронтендом через API‑маршрути

### Інфраструктура
- Очищено кеш Docker (`docker builder prune -a`) для усунення проблеми з пошкодженими шарами
- Пересобрано контейнер `rio_frontend` з параметром `--no-cache`
- Перевірено логи контейнера: Uvicorn успішно стартує і слухає порт 80 (localhost:3001)
- Відновлено стабільну роботу всіх контейнерів (frontend, backend1, backend2, node, db)
- Оновлено `env.prod` для узгодження конфігурацій між середовищами
- Прибрано зайве логування часу видачі токенів для оптимізації продуктивності
