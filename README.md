# Learning Projects — 9 Telegram-ботов на Python

Это портфолио: девять учебных проектов, сделанных по техническому заданию (файл `1.txt` в этом репозитории). Каждый проект живёт **в отдельном репозитории** — так удобнее и показывать, и развивать дальше. Здесь — индекс, ТЗ, валидатор и сводный дамп кода.

Я сознательно не добавлял в проекты ничего сверх библиотек из ТЗ: интересно было показать, что «продвинутость» — это не десять зависимостей, а чистая архитектура, тесты и умение бороться с реальными граблями.

## Проекты

| № | Репозиторий | Что делает | Стек |
|---|-------------|-----------|------|
| 1 | [wb-price-tracker](https://github.com/d3c0r1x/wb-price-tracker) | Следит за ценой/остатками на Wildberries, шлёт уведомления | aiogram v3, httpx, curl_cffi, aiosqlite, apscheduler |
| 2 | [ai-review-analyst](https://github.com/d3c0r1x/ai-review-analyst) | Топ-3 проблемы и преимущества товара из 50 отзывов (LLM + строгий JSON) | aiogram, httpx, openai/yandex, pydantic |
| 3 | [pdf-sales-reports](https://github.com/d3c0r1x/pdf-sales-reports) | PDF-отчёт по продажам: CSV → pandas → matplotlib → reportlab → Telegram | pandas, matplotlib, reportlab, aiogram |
| 4 | [telegram-stars-payment-gateway](https://github.com/d3c0r1x/telegram-stars-payment-gateway) | Подписка на AI-функции через Telegram Stars / ЮKassa (тест) | aiogram (PreCheckoutQuery, SuccessfulPayment), aiosqlite |
| 5 | [telegram-quiz-bot](https://github.com/d3c0r1x/telegram-quiz-bot) | Викторина: OpenTDB, инлайн-кнопки, лидерборд | aiogram v3, httpx, aiosqlite, pydantic |
| 6 | [currency-rate-bot](https://github.com/d3c0r1x/currency-rate-bot) | Курсы ЦБ РФ: XML-парсинг, конвертация, история, алерты | aiogram v3, httpx, apscheduler, aiosqlite, xml.etree |
| 7 | [telegram-weather-bot](https://github.com/d3c0r1x/telegram-weather-bot) | Погода и прогноз на 7 дней через Open-Meteo (без ключа) | aiogram v3, httpx, apscheduler, aiosqlite |
| 8 | [telegram-expense-tracker](https://github.com/d3c0r1x/telegram-expense-tracker) | Учёт расходов: `/add`, автокатегоризация, отчёты, CSV для Excel | aiogram v3, aiosqlite, stdlib csv |
| 9 | [telegram-news-bot](https://github.com/d3c0r1x/telegram-news-bot) | RSS/Atom ленты, дедупликация, ежедневный дайджест | aiogram v3, httpx, aiosqlite, xml.etree, apscheduler |

## Что внутри этого репозитория

- `1.txt` — техническое задание на все 9 проектов (библиотеки и методы);
- `_validate.py` — валидатор: прогоняет каждый проект изолированно, в отдельном процессе (`.venv/Scripts/python _validate.py p1|p2|...|p9`);
- `ves_kod_proektov.txt` — сводный дамп кода всех проектов;
- папки `project1_...`–`project9_...` — рабочие копии, каждая со своим git-репозиторием и GitHub Actions CI.

## Что общего у всех проектов

- **aiogram v3 middlewares** — троттлинг (защита от спама) и логирование;
- **TTL-кэши и retry с джиттером** — на чистом stdlib, без дополнительных библиотек;
- **кулдауны уведомлений и плановая очистка БД** — базы и память не растут вечно;
- **тесты и CI** — `pytest` + `compileall` на каждый push в каждом репозитории;
- **Dockerfile и pyproject.toml** — можно запустить где угодно.

Итого **67 unit-тестов** (9+7+7+5+10+8+7+8+6) + изолированный валидатор. В каждом README — честные «грабли», на которые я наступил, и планы.

## Честные примечания о публичных API (проверено 2026-08-05/06)

1. **Wildberries** (`card.wb.ru`, `feedbacks1.wb.ru`) — публичные, но недокументированные и антибот-защищённые: при прямой проверке вернули 403/пустой ответ. Поэтому в Проектах 1–2 есть демо-режим (`WB_DEMO_MODE=1`) и клиент с имитацией Chrome (`curl_cffi`) с поддержкой прокси. Для продакшена — официальный Seller API WB.
2. **OpenTDB** (Проект 5) — бесплатный без ключа; при перегрузке (`response_code=1`) бот откатывается на встроенный оффлайн-пул.
3. **ЦБ РФ** (Проект 6) — официальный бесплатный XML; нюансы: windows-1251 (парсим байты), десятичная запятая, `Nominal` для «дорогих» валют.
4. **Open-Meteo** (Проект 7) — бесплатный без ключа; прогноз кэшируется (TTL 30 мин), есть оффлайн-демо.
5. **RSS/Atom** (Проект 9) — публичные ленты; парсер устойчив к namespace, кодировкам и кривым лентам.

## Запуск

Каждый проект независим, запускается из своей папки:

```bash
cd project7_telegram_weather_bot
pip install -r requirements.txt
export WEATHER_BOT_TOKEN=123456:ABC...   # токен от @BotFather
python bot.py
```

Нужен только токен бота от @BotFather — переменные окружения описаны в `.env.example` каждой папки. На Windows проще: `run_botN.cmd` сам читает `TG_TOKEN` из корневого `.env` и запускает бота из `.venv`.

## Связки между проектами

- **1 → 2**: оба ходят в публичные API WB (карточки и отзывы);
- **4 → 2**: Проект 4 открывает доступ к AI-анализу Проекта 2 после оплаты (`ai_service.py` импортирует его модули, если папка рядом);
- **5–9**: независимые боты на бесплатных публичных API без ключей.

## Что дальше (идеи для новых проектов)

- бот для напоминаний/трекеров привычек;
- агрегатор цен с одного товара по разным маркетплейсам;
- «техподдержка» на базе FAQ-базы в SQLite.
