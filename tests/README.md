# 🧩 Проект автоматизированного тестирования приложения **Niffler**
<img src="/niffler-ng-client/src/assets/images/niffler-with-a-coin.png" width="250">

---

## 🚀 Быстрый старт
Для запуска проекта необходимо установить docker и Java 21
### 💻 Для macOS / Linux

```bash
# Клонировать репозиторий
git clone https://github.com/Andreyshabalinn/niffler-py-st3.git
cd niffler-py-st3

# Установить зависимости
pip install -r tests/requirements.txt

# Собрать и запустить систему Niffler
bash docker-compose-dev.sh
```

---

## ⚙️ Технологии проекта

- ✅ python
- ✅ pytest
- ✅ playwright
- ✅ allure
- ✅ kafka
- ✅ postgres
- ✅ poetry
- ✅ github
- ✅ pycharm
- ✅ Requests
- ✅ SQLAlchemy
- ✅ Jinja2

---

## 🧭 Структура проекта

```
niffler-py-st3/
│
├── docker-compose-dev.sh           # Сборка и запуск контейнеров Niffler
├── tests/
│   ├── fixtures/                   # Pytest-фикстуры (UI, API, DB, Kafka, gRPC)
│   ├── pages/                      # PageObject модели для Playwright UI тестов
│   ├── grpc_tests/                 # gRPC тесты
│   ├── databases/                  # Подключения к PostgreSQL (SQLModel)
│   ├── utils/                      # Клиенты Kafka, AuthClient, Allure-хелперы
│   ├── models/                     # Pydantic-конфиги и DTO
│   ├── .env                        # Переменные окружения
│   └── allure-results/, allure-report/ # Allure результаты и отчёты
│
└── .github/workflows/ci.yml        # GitHub Actions CI/CD с Allure Report
```

---

## 🔍 Основные особенности

- ✅ **UI-тесты** на фреймворке `Playwright` с использованием Page Object Model и Page Factory. Также добавлены UI тесты + DB с использованием передачи данных REST API
- ✅ **API-тесты** проверяющие интеграцию REST API и SOAP с авторизацией, токенами и JSON-валидацией  (библиотеки Request, HTTPX)
- ✅ **E2E-тесты** проверяющие очередь и обработку событий Kafka → DB → API
- ✅ **Фикстуры** для управления запуском тестов и подготовкой тестовых данных
- ✅ **Pydantic** для валидации и трансформации данных 
- ✅ **SQLModel + PostgreSQL+ SQLAlchemy** для управления и взаимодействия с БД и валидации данных 
- ✅ Поддержка **headless-режима** и CI-запусков. Поддержка параллельного запуска тестов
- ✅ **gRPC-тесты** с мок-сервером через Docker 
- ✅ **Allure-отчёты** с кастомными CSS-вложениями 
- ✅ **Jinja2** шаблонизатор для повышения читаемости отчетов тестирования

---

## 🧪 Подготовка окружения тестов

Тестовые настройки `.env` в папке `tests/`:

```
TOKEN=asd
BASE_URL=http://frontend.niffler.dc/
BASE_AUTH_URL=http://auth.niffler.dc:9000/
API_BASE_URL=http://gateway.niffler.dc:8090/api/
TEST_LOGIN=asd
TEST_PASSWORD=asd
DB_URL=postgresql://postgres:secret@localhost:5432/niffler-spend
USER_DB_URL=postgresql://postgres:secret@localhost:5432/niffler-userdata
AUTH_SECRET=Y2xpZW50OnNlY3JldA==
SERVER_NAME=localhost
SOAP_ADDRESS=http://localhost:8089/ws
```

---

### Примеры команд:

| Назначение | Команда |
|-------------|----------|
| Все тесты | `pytest -s -v tests/ --alluredir=./allure-results` |
| Параллельно (4 потока) | `pytest -n 4 -s -v tests/test_api_with_db.py --alluredir=./allure-results --dist=loadscope` |
| gRPC с моками | `pytest -s -v tests/grpc_tests --alluredir=./allure-results --mock` |

Перед `--mock` запусти мок-сервис:
```bash
docker-compose -f docker-compose.mock.yml up -d
```

---

## 🤖 CI/CD и GitHub Pages

- Запускается при Pull Request и коммитах в `main`
- Автоматически поднимает Docker, Playwright и Allure
- После прогона формирует Allure Report
- **Публикует отчёт на [GitHub Pages](https://andreyshabalinn.github.io/niffler-py-st3/)**

---

## 📘 Автор и контакты

👤 **Андрей Шабалин**  
🧠 Python QA Automation Engineer
🗓️ 2025  
📧 Email: andreyshabalin34@gmail.com   
💼 [LinkedIn](https://www.linkedin.com/in/andrey-shabalin-qa/)  
