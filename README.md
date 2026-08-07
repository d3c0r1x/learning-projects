# Learning Projects: 6 Telegram-ботов на Python

По файлу `1.txt` (ТЗ) реализованы **6 учебных проектов**. Каждый проект —
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

## Что внутри этого репозитория

- `1.txt` — техническое задание на все 6 проектов (библиотеки и методы);
- `_validate.py` — валидатор: прогоняет каждый проект изолированно
  (`.venv/Scripts/python _validate.py p1|p2|...|p6`);
- `ves_kod_proektov.txt` — сводный дамп кода всех проектов;
- папки `project1_...`–`project6_...` — рабочие копии, каждая со своим
  git-репозиторием, запушенным на GitHub.

## Связка проектов

- **1 → 2**: Проект 1 ходит в тот же публичный API карточек WB
  (`card.wb.ru`), который Проект 2 использует для получения `root_id` отзывов.
- **4 → 2**: Проект 4 открывает доступ к AI-анализу Проекта 2 после оплаты
  подписки (`ai_service.py` импортирует модули Проекта 2, если папка рядом).
- **5, 6**: независимые боты на бесплатных публичных API без ключей —
  запускаются сразу после установки зависимостей.

## Запуск

Каждый проект независим и запускается из своей папки:

```bash
cd project5_telegram_quiz_bot && pip install -r requirements.txt && python bot.py
# ...аналогично для project1/2/3/4/6
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
