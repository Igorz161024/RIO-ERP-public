# RIO-ERP
ERP‑система дипломного проєкту. Бекенд на FastAPI, фронтенд на RIO.

---

## Опис
RIO-ERP — це ERP‑система з бекендом на FastAPI та фронтендом на RIO.  
Проєкт створений для дипломної роботи та подальшого розвитку у продакшн‑середовищі.

---

## Структура
- **backend/** — бекенд на FastAPI + SQLAlchemy + Alembic
- **frontend_rio/** — фронтенд на RIO
- **docker-compose.yml** — конфігурація контейнерів (Postgres, бекенд, фронтенд, nginx, backup)
- **CHANGELOG.md** — історія змін
- **README.md** — інструкції запуску

---

## Вимоги
- Windows 11 + WSL2 (Ubuntu)
- Docker + Docker Compose
- Git
- Python 3.11 (для локальних тестів)

---

## Покроковий запуск на іншому ПК

### 1. Клонування репозиторію
```bash
    git clone https://github.com/Igorz161024/RIO-ERP-public.git
cd RIO-ERP
2. Запуск контейнерів
bash
    docker compose up -d --build
3. Перевірка статусу контейнерів
bash
    docker ps
→ усі сервіси мають бути у статусі healthy.
4. Запуск фронтенду
bash
    rio run --port 9000
Фронтенд буде доступний за адресою:
http://localhost:9000
5. Доступ до бекенду
Бекенд працює на порту 7000:
http://localhost:7000/docs — Swagger UI
6. Авторизація
Отримання токена:
bash
curl -X POST http://localhost:7000/token \
    -d "username=admin&password=admin123"
Збереження токена у PowerShell:
powershell
    $TOKEN = "<отриманий токен>"
7. CRUD‑операції
Users
bash
curl -X POST http://localhost:7000/api/users \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"username":"test","password":"1234","email":"test@example.com"}'
Finance
bash
curl -X POST http://localhost:7000/api/finance/add_entry \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"account_id":1,"amount":500,"operation":"income"}'  
    ---

## Бекапи
- Автоматичні бекапи створюються контейнером `rio_backup` у директорії `./backups`.
- Відновлення:
```bash
psql -U postgres -d erp_diplom < backups/erp_diplom_YYYYMMDD.sql
CHANGELOG
Останній реліз: v1.2.0

Узгоджено моделі Account, EntryLine, Journal.

Виправлено DELETE для Journal.

Healthcheck для всіх контейнерів → healthy.

Оптимізація Docker‑образів (multi‑stage build, .dockerignore).

Автоматичні бекапи підтверджені.

CRUD‑операції стабільні.
