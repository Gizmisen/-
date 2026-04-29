# PMZ AI Control

Рабочий MVP backend на FastAPI + PostgreSQL для:
- регистрации/логина;
- загрузки Excel;
- сохранения сырых строк импорта;
- импорта `plan` и `fact`;
- отчёта план-факт.

## Запуск

```bash
cd pmz-ai-control
docker compose up --build
```

Проверка:
- `GET http://localhost:8000/health`
- Swagger: `http://localhost:8000/docs`
- MVP интерфейс: `http://localhost:8000/`

## Основные API

1. `POST /auth/register`
2. `POST /auth/login`
3. `POST /imports/upload` (form-data: `module=plan|fact`, `file=<excel>`)
4. `GET /imports/{file_id}/preview`
5. `POST /imports/{file_id}/confirm` (form-data: `sheet_name=...`)
6. `GET /plan-fact?period=2026-03`
7. `POST /ai/query` (json: `{ "query": "Что не закрыто по заказу 102100118179?" }`)

## Формат Excel для MVP

### module=plan
Колонки:
- `plan_period`, `plan_version`, `order_number`, `material_code`, `material_name`,
- `plant`, `department`, `work_center`, `planned_qty`, `planned_hours`, `planned_weight`.

### module=fact
Колонки:
- `fact_period`, `order_number`, `customer_order`, `material_code`, `material_name`,
- `plant`, `department`, `work_center`, `order_qty`, `delivered_qty`, `confirmed_qty`, `fact_qty`, `fact_hours`.


## Запуск как EXE (Windows)

1. Откройте `cmd` в папке `pmz-ai-control`.
2. Выполните:

```bat
build_exe.bat
```

3. После сборки появится `dist\pmz-ai-control.exe`.
4. Запустите EXE и откройте `http://localhost:8000`.

## Быстрый локальный запуск (Linux/macOS)

```bash
./run_local.sh
```

## Запуск в 2 клика (Windows)

- Двойной клик по `start_pmz.bat`:
  - если EXE уже собран — сразу запускается приложение и открывается браузер;
  - если EXE не собран — сначала автоматически выполняется сборка, потом запуск.

Для режима разработки (без EXE): двойной клик по `start_pmz_dev.bat`.
