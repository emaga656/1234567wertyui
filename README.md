# TaskFlow — финальный проект КТ6

Backend-приложение на FastAPI для управления проектами и задачами. Реализованы четыре функциональных модуля: Authentication, Projects, Tasks, Notifications.

## Что реализовано по требованиям КТ6

- FastAPI и модульная структура: роутеры, сервисная логика и Pydantic-схемы.
- PostgreSQL + SQLAlchemy 2.0; таблицы `users`, `projects`, `tasks`, `notifications`; связи один-ко-многим.
- Alembic: начальная миграция `0001_initial.py`; автоматический `create_all` не используется.
- Регистрация с bcrypt-хешированием; OAuth2 Password Flow (`/auth/login`) и JWT.
- RBAC: удаление проекта (`DELETE /projects/{project_id}`) доступно только роли `admin`.
- CORS с явным списком origin из `CORS_ORIGINS`.
- Rate limit на вход: значение `RATE_LIMIT_LOGIN`, по умолчанию 5 запросов в минуту на IP.
- Celery + Redis: при создании проекта ставится фоновая задача, которая создаёт in-app уведомление; просмотр через `/notifications`.
- Docker Compose запускает API, PostgreSQL, Redis и Celery worker.
- GitHub Actions запускает миграции и тесты при push и pull request.
- Подготовлен `railway.toml` для деплоя на Railway.

## Запуск на Windows

1. Установить Docker Desktop и запустить его.
2. В корне проекта создать `.env` копированием `.env.example`:
   ```powershell
   Copy-Item .env.example .env
   ```
3. При первом запуске поменять `SECRET_KEY`, `ADMIN_PASSWORD`, `ADMIN_EMAIL` в `.env`.
4. Запустить всё одной командой:
   ```powershell
   docker compose up --build
   ```
5. Открыть Swagger: http://localhost:8000/docs . Проверка: http://localhost:8000/health .

Остановка: `Ctrl+C`, затем `docker compose down`. Для удаления данных БД: `docker compose down -v`.

## Как проверить API в Swagger

1. `POST /auth/register` — создать обычного пользователя:
   ```json
   {"email":"student@example.com","password":"Student123!"}
   ```
2. `POST /auth/login` — OAuth2 форма, в поле `username` указать email, в `password` — пароль. Скопировать `access_token`.
3. Нажать **Authorize** и вставить токен (или `Bearer <token>`, если интерфейс просит префикс).
4. `POST /projects`:
   ```json
   {"name":"Учебный проект","description":"Проверка API TaskFlow"}
   ```
5. `POST /projects/{project_id}/tasks`:
   ```json
   {"title":"Сделать КТ6","description":"Проверить требования задания"}
   ```
6. `GET /projects/{project_id}/tasks` — получить задачи проекта.
7. `PATCH /tasks/{task_id}`:
   ```json
   {"status":"done"}
   ```
   Допустимые статусы: `todo`, `in_progress`, `done`.
8. Через несколько секунд `GET /notifications` покажет уведомление о создании проекта (работает Celery worker).

## Создание администратора

После запуска контейнеров выполнить:

```powershell
docker compose exec app python -c "from app.db.session import SessionLocal; from app.models import User; from app.core.security import hash_password; from app.core.config import settings; db=SessionLocal(); u=db.query(User).filter(User.email==settings.admin_email).first(); u= u or User(email=settings.admin_email, hashed_password=hash_password(settings.admin_password), role='admin'); u.role='admin'; db.add(u); db.commit(); print('Admin ready:', u.email); db.close()"
```

Затем войти через `/auth/login` с `ADMIN_EMAIL` и `ADMIN_PASSWORD`. Важно: не используйте демонстрационный пароль в опубликованном проекте.

## Полезные команды

```powershell
docker compose ps
docker compose logs -f app
docker compose logs -f worker
docker compose exec app alembic current
docker compose exec app pytest -q
```

## Деплой на Railway

1. Загрузить проект в собственный GitHub-репозиторий.
2. В Railway создать проект из GitHub-репозитория и добавить PostgreSQL и Redis.
3. Для сервиса приложения указать команду запуска:
   `sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"`
4. Для сервиса worker использовать тот же репозиторий и команду:
   `celery -A app.celery_app.celery worker --loglevel=info`.
5. В Variables приложения и worker задать `DATABASE_URL` (Railway PostgreSQL URL, привести к драйверу `postgresql+psycopg://`), `REDIS_URL`, `SECRET_KEY`, `CORS_ORIGINS`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`. Приложению Railway назначить публичный домен и порт `$PORT`.
6. После деплоя проверить `/health` и `/docs` по публичному домену.

Публичный URL и факт успешного деплоя нельзя заранее подставить в проект: они появятся только после деплоя в вашем Railway-аккаунте.

## Структура

```text
app/
  core/                 # конфигурация, безопасность, зависимости
  db/                   # SQLAlchemy Base и сессия
  modules/
    auth/               # регистрация, вход, профиль
    projects/           # CRUD проектов
    tasks/              # CRUD задач и статусы
    notifications/      # список уведомлений
  models.py             # ORM-модели и связи
  celery_app.py         # Celery
  tasks.py              # фоновая задача
  main.py               # приложение и middleware
alembic/                # миграции
.github/workflows/      # CI
Dockerfile
docker-compose.yml
```
