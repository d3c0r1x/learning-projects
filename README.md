# Learning Projects — 11 Telegram-ботов на Python

Одиннадцать учебных проектов, реализованных по техническому заданию (файл `1.txt` в этом репозитории). Каждый проект размещён **в отдельном репозитории** — для независимого использования и дальнейшего развития. Данный репозиторий содержит индекс, ТЗ, валидатор и сводный дамп кода.

В проектах используются только библиотеки, указанные в техническом задании.

## Проекты

| № | Репозиторий | Назначение | Стек |
|---|-------------|-----------|------|
| 1 | [wb-price-tracker](https://github.com/d3c0r1x/wb-price-tracker) | Мониторинг цен и остатков на Wildberries с уведомлениями | aiogram v3, httpx, curl_cffi, aiosqlite, apscheduler |
| 2 | [ai-review-analyst](https://github.com/d3c0r1x/ai-review-analyst) | Топ-3 проблемы и преимущества товара из 50 отзывов (LLM + строгий JSON) | aiogram, httpx, openai/yandex, pydantic |
| 3 | [pdf-sales-reports](https://github.com/d3c0r1x/pdf-sales-reports) | PDF-отчёт по продажам: CSV → pandas → matplotlib → reportlab → Telegram | pandas, matplotlib, reportlab, aiogram |
| 4 | [telegram-stars-payment-gateway](https://github.com/d3c0r1x/telegram-stars-payment-gateway) | Подписка на AI-функции через Telegram Stars / ЮKassa (тест) | aiogram (PreCheckoutQuery, SuccessfulPayment), aiosqlite |
| 5 | [telegram-quiz-bot](https://github.com/d3c0r1x/telegram-quiz-bot) | Викторина: OpenTDB, инлайн-кнопки, лидерборд | aiogram v3, httpx, aiosqlite, pydantic |
| 6 | [currency-rate-bot](https://github.com/d3c0r1x/currency-rate-bot) | Курсы ЦБ РФ: XML-парсинг, конвертация, история, алерты | aiogram v3, httpx, apscheduler, aiosqlite, xml.etree |
| 7 | [telegram-weather-bot](https://github.com/d3c0r1x/telegram-weather-bot) | Погода и прогноз на 7 дней через Open-Meteo (без ключа) | aiogram v3, httpx, apscheduler, aiosqlite |
| 8 | [telegram-expense-tracker](https://github.com/d3c0r1x/telegram-expense-tracker) | Учёт расходов: `/add`, автокатегоризация, отчёты, CSV для Excel | aiogram v3, aiosqlite, stdlib csv |
| 9 | [telegram-news-bot](https://github.com/d3c0r1x/telegram-news-bot) | RSS/Atom ленты, дедупликация, ежедневный дайджест | aiogram v3, httpx, aiosqlite, xml.etree, apscheduler |
| 10 | [ozon-price-tracker](https://github.com/d3c0r1x/ozon-price-tracker) | Мониторинг цен и остатков на Ozon: падение цены, возврат в наличие, пороги | aiogram v3, httpx, curl_cffi, aiosqlite, apscheduler |
| 11 | [marketplace-price-compare](https://github.com/d3c0r1x/marketplace-price-compare) | Сравнение цен WB и Ozon: поиск, лучшая цена, watch-подписки на падение цены | aiogram v3, httpx, curl_cffi, aiosqlite, apscheduler, pydantic |

## Содержимое репозитория

- `1.txt` — техническое задание на все 11 проектов (библиотеки и методы);
- `_validate.py` — валидатор: изолированный запуск каждого проекта в отдельном процессе (`.venv/Scripts/python _validate.py p1|p2|...|p11`);
- `ves_kod_proektov.txt` — сводный дамп кода всех проектов;
- папки `project1_...`–`project11_...` — рабочие копии, каждая со своим git-репозиторием и GitHub Actions CI.

## Общие элементы всех проектов

- **aiogram v3 middlewares** — троттлинг (защита от спама) и логирование;
- **TTL-кэши и retry с джиттером** — на чистом stdlib, без дополнительных библиотек;
- **кулдауны уведомлений и плановая очистка БД** — контролируемый рост баз и памяти;
- **тесты и CI** — `pytest` + `compileall` при каждом push в каждом репозитории;
- **Dockerfile и pyproject.toml** — возможность запуска в любом окружении.

Итого **102 unit-теста** (9+7+7+5+10+8+7+8+6+16+19) + изолированный валидатор. В каждом README — раздел «Технические особенности» с описанием выявленных ограничений и решений, а также «Планы развития».

## Примечания о публичных API (проверено 2026-08-05/08)

1. **Wildberries** (`card.wb.ru`, `search.wb.ru`, `feedbacks1.wb.ru`) — публичные, но недокументированные и защищённые антиботом: при прямой проверке возвращали 403/429/пустой ответ. Поэтому в Проектах 1–2 и 11 предусмотрен демо-режим и клиент с имитацией Chrome (`curl_cffi`) с поддержкой прокси.
2. **Ozon** (`www.ozon.ru/api/composer-api.bx/page/json/v2`, Проекты 10–11) — публичный composer-api; без валидного region-cookie возвращает HTTP 307 (редирект-петля антибота). Ответ — `widgetStates` с JSON-строками внутри; парсеры устойчивы к смене структуры. Реальные данные — через прокси или демо-режим.
3. **OpenTDB** (Проект 5) — бесплатный без ключа; при перегрузке (`response_code=1`) бот переключается на встроенный оффлайн-пул.
4. **ЦБ РФ** (Проект 6) — официальный бесплатный XML; особенности: windows-1251 (парсинг байтов), десятичная запятая, `Nominal` для валют с большим номиналом.
5. **Open-Meteo** (Проект 7) — бесплатный без ключа; прогноз кэшируется (TTL 30 мин), предусмотрен оффлайн-демо.
6. **RSS/Atom** (Проект 9) — публичные ленты; парсер устойчив к namespace, кодировкам и отклонениям от спецификации.

## Запуск

Каждый проект независим, запускается из своей папки:

```bash
cd project10_ozon_price_tracker
pip install -r requirements.txt
export OZON_BOT_TOKEN=123456:ABC...   # токен от @BotFather
python bot.py
```

Требуется только токен бота от @BotFather — переменные окружения описаны в `.env.example` каждой папки. На Windows проще: `run_botN.cmd` самостоятельно читает `TG_TOKEN` из корневого `.env` и запускает бота из `.venv`.

## Связи между проектами

- **1 → 2**: оба обращаются к публичным API WB (карточки и отзывы);
- **1, 10, 11**: трекер WB, трекер Ozon и компаратор WB↔Ozon образуют линейку инструментов для работы с маркетплейсами (адаптеры WB в 1 и 11 построены на одном эндпоинте `search.wb.ru`);
- **4 → 2**: Проект 4 открывает доступ к AI-анализу Проекта 2 после оплаты (`ai_service.py` импортирует его модули, если папка расположена рядом);
- **5–9**: независимые боты на бесплатных публичных API без ключей.

## Идеи для развития

- бот для напоминаний/трекеров привычек;
- «техподдержка» на основе FAQ-базы в SQLite;
- Yandex Market как третий маркетплейс в компараторе (публичное API с бесплатным ключом).
