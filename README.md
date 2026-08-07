# Learning Projects: 9 Telegram-ботов на Python

По файлу `1.txt` (ТЗ) реализованы **9 учебных проектов**. Каждый проект —
**в отдельном репозитории**; этот репозиторий — индекс-портфолио
(ТЗ, валидатор, сводный дамп кода).

## Репозитории

| № | Репозиторий | Суть | Стек |
|---|-------------|------|------|
| 1 | [wb-price-tracker](https://github.com/d3c0r1x/wb-price-tracker) | Трекер цен/остатков Wildberries с push-уведомлениями раз в сутки | aiogram v3, httpx, curl_cffi, aiosqlite, asyncio, apscheduler |
| 2 | [ai-review-analyst](https://github.com/d3c0r1x/ai-review-analyst) | AI-анализ 50 отзывов: топ-3 проблемы/преимущества (строгий JSON) | aiogram, httpx, openai, pydantic |
| 3 | [pdf-sales-reports](https://github.com/d3c0r1x/pdf-sales-reports) | PDF-отчёт по продажам: CSV → pandas → matplotlib → reportlab → Telegram | pandas, matplotlib, reportlab, aiogram |
| 4 | [telegram-stars-payment-gateway](https://github.com/d3c0r1x/telegram-stars-payment-gateway) | Подписка на AI-функции через Telegram Stars / ЮKassa (тест) | aiogram (PreCheckoutQuery, SuccessfulPayment) + SQLite |
| 5 | [telegram-quiz-bot](https://github.com/d3c0r1x/telegram-quiz-bot) | Викторина: вопросы OpenTDB, инлайн-кнопки, лидерборд в SQLite | aiogram v3, httpx, aiosqlite, pydantic |
| 6 | [currency-rate-bot](https://github.com/d3c0r1x/currency-rate-bot) | Курсы валют ЦБ РФ: XML-парсинг, конвертация, история, ежедневная рассылка | aiogram v3, httpx, apscheduler, aiosqlite, xml.etree |
| 7 | [telegram-weather-bot](https://github.com/d3c0r1x/telegram-weather-bot) | Погода и прогноз на 7 дней через Open-Meteo, ежедневная рассылка | aiogram v3, httpx, pydantic, apscheduler, aiosqlite |
| 8 | [telegram-expense-tracker](https://github.com/d3c0r1x/telegram-expense-tracker) | Учёт расходов: /add с автокатегоризацией, отчёты, экспорт CSV | aiogram v3, aiosqlite, stdlib csv |
| 9 | [telegram-news-bot](https://github.com/d3c0r1x/telegram-news-bot) | RSS/Atom ленты: дедупликация, ежедневный дайджест подписчикам | aiogram v3, httpx, aiosqlite, xml.etree, apscheduler |

## Что внутри этого репозитория

- `1.txt` — техническое задание на все 9 проектов (библиотеки и методы);
- `_validate.py` — валидатор: прогоняет каждый проект изолированно
  (`.venv/Scripts/python _validate.py p1|p2|...|p9`);
- `ves_kod_proektov.txt` — сводный дамп кода всех проектов;
- папки `project1_...`–`project9_...` — рабочие копии, каждая со своим
  git-репозиторием, запушенным на GitHub.

## Продвинутый уровень (v2)

Все 9 проектов — «продвинутые учебные», без лишних сторонних зависимостей,
только на библиотеках из ТЗ:

- **aiogram v3 middlewares** во всех ботах: троттлинг (спам-защита) и логирование;
- **TTL-кэши и retry с джиттером** на чистом stdlib (`utils.py`);
- **кулдауны уведомлений, индексы и очистка БД** — базы не растут вечно;
- **цепи LLM-провайдеров с фолбэком** и переспрос при невалидном JSON (P2);
- **таблицы Platypus, многопанельные графики и CLI** (P3);
- **тарифы, пробный период и возвраты Stars** (P4);
- **выбор сложности, пагинация лидерборда, точность в %** (P5);
- **watchlist и пороговые алерты курсов** с часовым джобом (P6);
- **namespace-агностичный парсер RSS/Atom** и дедупликация по `UNIQUE(link)` (P9);
- **агрегаты в SQL** (GROUP BY/BETWEEN) и CSV с BOM для Excel (P8);
- **чистые функции парсинга Open-Meteo** под unit-тесты (P7);
- **операции**: `pyproject.toml`, `Dockerfile`, GitHub Actions CI в каждом репо.

Итого **64 unit-теста** (9+7+7+5+7+8+7+8+6) + изолированный валидатор
`_validate.py`.

## Связка проектов

- **1 → 2**: Проект 1 ходит в тот же публичный API карточек WB
  (`card.wb.ru`), который Проект 2 использует для получения `root_id` отзывов.
- **4 → 2**: Проект 4 открывает доступ к AI-анализу Проекта 2 после оплаты
  подписки (`ai_service.py` импортирует модули Проекта 2, если папка рядом).
- **5, 6, 7, 8, 9**: независимые боты на бесплатных публичных API без ключей —
  запускаются сразу после установки зависимостей.

## Запуск

Каждый проект независим и запускается из своей папки:

```bash
cd project7_telegram_weather_bot && pip install -r requirements.txt && python bot.py
# ...аналогично для project1/2/3/4/5/6/8/9
```

Нужен только токен бота от @BotFather — переменные окружения описаны
в `.env.example` каждой папки (на Windows есть готовые `run_bot*.cmd`,
читающие `TG_TOKEN` из корневого `.env`).

## Честные примечания о публичных API (проверено 2026-08-05/06)

1. **Wildberries** (`card.wb.ru`, `feedbacks1.wb.ru`) — публичные, но
   недокументированные и антибот-защищённые: при прямой проверке с этого
   компьютера вернули 403/пустой ответ. Поэтому в Проектах 1–2 есть
   демо-режим (`WB_DEMO_MODE=1`), работающий без сети, а в Проекте 1 —
   клиент с имитацией Chrome (`curl_cffi`), поддержкой прокси и командой
   `/diag`. Для продакшена следует использовать официальный Seller API WB.
2. **OpenTDB** (Проект 5) — бесплатный API без ключа; при перегрузке
   (`response_code=1`) бот откатывается на встроенный оффлайн-пул.
3. **ЦБ РФ** (Проект 6) — официальный бесплатный XML без ключа; нюансы:
   кодировка windows-1251 (парсим байты), десятичная запятая, `Nominal`
   для «дорогих» валют.
4. **Open-Meteo** (Проект 7) — бесплатный API без ключа; бот кэширует
   прогноз (TTL 30 мин) и имеет оффлайн-демо.
5. **RSS/Atom ленты** (Проект 9) — публичные и бесплатные; парсер
   устойчив к namespace, кодировкам и «грязным» лентам.
