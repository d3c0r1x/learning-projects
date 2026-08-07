# Учебный проект: 4 Telegram-бота на Python (Wildberries)

По файлу `1.txt` реализованы **4 проекта** — каждый в своей папке, со строго
теми библиотеками и методами, что описаны в ТЗ.

| № | Папка                                        | Суть                                                        | Стек (по ТЗ)                                        |
|---|----------------------------------------------|-------------------------------------------------------------|-----------------------------------------------------|
| 1 | `project1_wb_price_tracker`                  | Трекер цен/остатков WB с уведомлениями раз в сутки          | aiogram v3, httpx, aiosqlite, asyncio, apscheduler  |
| 2 | `project2_ai_review_analyst`                 | AI-анализ 50 отзывов: топ-3 проблемы/преимущества (JSON)    | aiogram, httpx, yandex-cloud-ml-sdk (или openai), pydantic |
| 3 | `project3_pdf_reports`                       | PDF-отчёт по продажам: CSV → pandas → matplotlib → reportlab → Telegram | pandas, matplotlib, reportlab, aiogram |
| 4 | `project4_payment_gateway`                   | Подписка на AI-функции через Telegram Stars / ЮKassa (тест) | aiogram (PreCheckoutQuery, SuccessfulPayment) + SQLite |

## Связка проектов

- **1 → 2**: Проект 1 ходит в тот же публичный API карточек WB
  (`card.wb.ru`), который Проект 2 использует для получения `root_id` отзывов.
- **4 → 2**: Проект 4 открывает доступ к AI-анализу Проекта 2 после оплаты
  подписки (`ai_service.py` импортирует модули Проекта 2, если папка рядом).

## Запуск

Каждый проект независим:

```bash
cd project1_wb_price_tracker && pip install -r requirements.txt && python bot.py
# ...аналогично для project2/3/4
```

Нужен только токен бота от @BotFather (`WB_BOT_TOKEN`), примеры переменных —
в `.env.example` каждой папки.

## Честные примечания о публичном API Wildberries (проверено 2026-08-05)

1. **Эндпоинт карточек** `card.wb.ru/cards/v1/detail` — публичный, но
   недокументированный. Его формат подтверждён open-source проектами
   ([joitandr/wb_parsing](https://github.com/joitandr/wb_parsing),
   [nickisnotgaara/wildberries-reviews-bot](https://github.com/nickisnotgaara/wildberries-reviews-bot)).
   **При прямой проверке с этого компьютера WB вернул 403 (антибот)** — поэтому
   в проектах есть демо-режим (`WB_DEMO_MODE=1`), работающий без сети.
2. **Эндпоинт отзывов** `feedbacks1.wb.ru/feedbacks/v1/{root_id}` — тоже
   недокументированный и антибот-защищённый; официальный
   `feedbacks-api.wildberries.ru` требует токен продавца. Парсер написан
   устойчивым к смене структуры JSON, проверка с этого компьютера была
   заблокирована (пустой ответ).
3. Цены WB приходят в **копейках** — код делит на 100.
4. Эндпоинты могут меняться в любой момент: это недокументированные API.
   Для продакшена следует использовать официальный Seller API WB.
