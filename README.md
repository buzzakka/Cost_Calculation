# CostCalculation

## Описание

`CostCalculation` - это веб-приложение, предназначенное для расчёта трат за месяц. Приложение позволяет пользователям легко вводить свои ежедневные расходы и автоматически рассчитывать их общую сумму за месяц, что помогает в планировании бюджета и финансовом учете.

## Настройка проекта

### Требования

Для работы с проектом вам понадобятся следующие инструменты:
- Python (версии 3.x)
- Django (последняя версия)
- Другие зависимости, указанные в файле `requirements.txt`
- Docker, docker-compose

### Установка зависимостей

Чтобы установить необходимые зависимости, выполните следующую команду в терминале:

```bash
pip install -r requirements.txt
```

### .env

Для работы необходимо создать файл `.env` в разделе с файлом `manage.py` со следующим содержимым:

```bash
# Django settings
DJANGO_SECRET_KEY=

DJANGO_DEBUG=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

DB_ENGINE=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Postgres settings
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Эти пары значений должны совпадать: `DB_NAME` и `POSTGRES_DB`, `DB_USER` и `POSTGRES_USER`, `DB_PASSWORD` и `POSTGRES_PASSWORD`. 

### Docker
Разверните контейнеры следующими командами:

```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --no-input --clear
```

Веб приложение будет доступно по адресу `http://127.0.0.1:1337/`.