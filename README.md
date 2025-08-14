# Suzy AI Pet

Эмоциональный AI-питомец с долгосрочной памятью и анализом эмоций пользователя.

## Описание

Suzy AI Pet - интеллектуальный агент на основе LangGraph, который анализирует эмоции пользователя, поддерживает долгосрочную память о разговорах и предоставляет эмоциональную поддержку. Система использует векторное хранилище PostgreSQL с расширением pgvector для семантического поиска.

## Архитектура

### Основные компоненты

- **Agents Graph** - граф агентов на основе LangGraph
- **Emotion Classifier** - классификатор эмоций на основе LLM
- **Suzy Tool** - основной мозг AI-питомца
- **Long-term Memory** - долгосрочная память с векторным поиском
- **Short-term Memory** - краткосрочная память для контекста разговора

### Структура проекта

```
SuzyAIPet/
├── src/
│   ├── agents/
│   │   ├── tools/
│   │   │   ├── emotion_classifier.py
│   │   │   └── suzy_tool.py
│   │   └── graph.py
│   ├── db/
│   │   └── create_db.py
│   ├── memory/
│   │   ├── lt_memory.py
│   │   └── st_memory.py
│   ├── utils/
│   │   ├── configs/
│   │   │   ├── config.yml
│   │   │   └── settings.py
│   │   ├── prompts.py
│   │   └── states.py
│   └── main.py
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

## Установка и настройка

### Предварительные требования

- Python 3.8+
- PostgreSQL 12+ с расширением pgvector
- Together AI API ключ

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd SuzyAIPet
```

### 2. Создание виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных

#### Установка PostgreSQL с pgvector

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install postgresql-12-pgvector

# macOS
brew install postgresql
brew install pgvector
```

#### Создание базы данных

```bash
psql -U postgres
CREATE DATABASE lt_memory;
\c lt_memory
CREATE EXTENSION IF NOT EXISTS vector;
```

### 5. Настройка переменных окружения

```bash
cp .env.example .env
```

Отредактируйте `.env` файл:

```env
TOGETHER_API_KEY=your_together_api_key_here
DB_NAME=lt_memory
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Инициализация базы данных

```bash
python src/db/create_db.py
```

### 7. Настройка конфигурации

Отредактируйте `src/utils/configs/config.yml`:

```yaml
llms:
  together_api_key: ${TOGETHER_API_KEY}
  classifier_emotion_llm:
    model: "togethercomputer/llama-2-7b-chat"
    temperature: 0
    max_tokens: 50
  suzy:
    model: "togethercomputer/llama-2-7b-chat"
    temperature: 0.6
    max_tokens: 400
```

## Использование

### Запуск FastAPI сервера

```bash
python src/main.py
```

Сервер будет доступен по адресу: http://localhost:8000

### API Endpoints

#### POST /chat
Отправить сообщение AI-питомцу

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user123",
       "message": "Сегодня я чувствую себя грустно"
     }'
```

#### GET /user/{user_id}/emotions
Получить последние эмоции пользователя

```bash
curl "http://localhost:8000/user/user123/emotions?limit=5"
```

#### DELETE /user/{user_id}/memory
Очистить память пользователя

```bash
curl -X DELETE "http://localhost:8000/user/user123/memory"
```

### Использование в коде

```python
from src.agents.graph import SuzyAI
from src.utils.states import GlobalState

state = GlobalState(
    user_id="user123",
    query="Привет, как дела?",
    answer="",
    emotion=""
)

final_state = SuzyAI.graph.invoke(state)
print(f"Ответ: {final_state.answer}")
print(f"Эмоция: {final_state.emotion}")
```

## Структура базы данных

### Таблица diary_entries
```sql
CREATE TABLE diary_entries (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    entry TEXT NOT NULL,
    emotion TEXT
);
```

### Векторное хранилище lt_memory
Хранит векторные представления сообщений для семантического поиска

## Конфигурация

### Модели LLM
- **Emotion Classifier**: Llama-2-7b-chat для классификации эмоций
- **Suzy Tool**: Llama-2-7b-chat для генерации ответов

### Параметры моделей
- **Temperature**: 0 для классификатора, 0.6 для генерации
- **Max Tokens**: 50 для классификатора, 400 для генерации

## Разработка

### Добавление новых функций

1. Создайте новый инструмент в `src/agents/tools/`
2. Добавьте узел в граф в `src/agents/graph.py`
3. Обновите промпты в `src/utils/prompts.py` при необходимости

### Тестирование

```bash
python -m pytest tests/
mypy src/
flake8 src/
```

## Безопасность

### Переменные окружения
- Никогда не коммитьте `.env` файл
- Используйте секреты для продакшена
- Ротация API ключей

### База данных
- Используйте отдельного пользователя для приложения
- Ограничьте права доступа
- Регулярные бэкапы

## Лицензия

MIT License

## Поддержка

Для вопросов и предложений создавайте Issues в репозитории.
