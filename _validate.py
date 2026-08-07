"""Валидация проектов. Запускать ПО ОДНОМУ ПРОЕКТУ на процесс:
    .venv/Scripts/python _validate.py p1|p2|...|p9

Каждый проект проверяется изолированно (как при реальном запуске), поэтому
коллизии одноимённых модулей (config.py, db.py) исключены.
"""
from __future__ import annotations

import asyncio
import os
import sys
import tempfile

PROJECTS = {
    "p1": "project1_wb_price_tracker",
    "p2": "project2_ai_review_analyst",
    "p3": "project3_pdf_reports",
    "p4": "project4_payment_gateway",
    "p5": "project5_telegram_quiz_bot",
    "p6": "project6_currency_rate_bot",
    "p7": "project7_telegram_weather_bot",
    "p8": "project8_telegram_expense_tracker",
    "p9": "project9_telegram_news_bot",
}


def _insert(project: str) -> None:
    sys.path.insert(0, PROJECTS[project])


def validate_p1() -> None:
    _insert("p1")
    from db import Database
    from wb_api import MockWBClient

    async def run() -> None:
        db = Database(os.path.join(tempfile.gettempdir(), "smoke_tracker.db"))
        if os.path.exists(db.path):
            os.remove(db.path)
        await db.init()
        card = await MockWBClient().get_card(17457977)
        assert card["salePriceU"] // 100 == 699
        await db.upsert_item(card)
        await db.track(111, "17457977")
        assert await db.list_tracked(111)
        assert await db.history("17457977")
        assert await db.users_for_articul("17457977") == [111]
        assert await db.untrack(111, "17457977")

    asyncio.run(run())
    print("  [OK] БД + mock-клиент + полный цикл трекинга")


def validate_p2() -> None:
    _insert("p2")
    from llm import MockProvider, extract_json
    from models import AnalysisResult
    from reviews import mock_reviews

    async def run() -> None:
        revs = mock_reviews(50)
        assert len(revs) == 50
        res = await MockProvider().analyze(revs)
        assert isinstance(res, AnalysisResult)
        assert len(res.pros) == 3 and len(res.cons) == 3
        assert 0.0 <= res.average_rating <= 5.0
        j = extract_json('```json\n{"pros": ["a"], "cons": ["b"], '
                         '"sentiment": "neutral", "average_rating": 3.5}\n```')
        assert j["pros"] == ["a"]

    asyncio.run(run())
    print("  [OK] mock-отзывы (50) + LLM + pydantic-валидация + extract_json")


def validate_p3() -> None:
    _insert("p3")
    from report import aggregate_sales, build_chart, build_pdf

    with tempfile.TemporaryDirectory() as tmp:
        csv_path = os.path.join(tmp, "sales.csv")
        chart_path = os.path.join(tmp, "top10.png")
        pdf_path = os.path.join(tmp, "report.pdf")
        # report.py генерирует CSV сам, если его нет
        report = aggregate_sales(csv_path)
        assert report.total_revenue > 0 and report.margin_percent > 0
        build_chart(report, chart_path)
        build_pdf(report, pdf_path, chart_path)
        assert os.path.getsize(pdf_path) > 1000
        assert os.path.getsize(chart_path) > 1000
        print("  [OK] CSV (чанки) -> pandas -> matplotlib -> reportlab (PDF) в темповой папке")


def validate_p4() -> None:
    _insert("p4")
    from ai_service import run_analysis
    from db import Database

    async def run() -> None:
        db = Database(os.path.join(tempfile.gettempdir(), "smoke_sub.db"))
        if os.path.exists(db.path):
            os.remove(db.path)
        await db.init()
        assert not await db.is_subscribed(555)
        await db.activate(555, "testuser", 30)
        assert await db.is_subscribed(555)
        assert await db.until(555)
        await db.deactivate(555)
        assert not await db.is_subscribed(555)
        print("  [OK] SQLite-подписки (activate/is_subscribed/deactivate)")

        # интеграция с Проектом 2 (реальный сценарий из bot.py)
        text = await run_analysis()
        assert "Результат AI-анализа" in text and "Преимущества" in text
        print("  [OK] Интеграция П4 -> П2 (ai_service загружает модули П2)")

    asyncio.run(run())


def validate_p5() -> None:
    _insert("p5")
    from db import Database
    from quiz_api import DEMO_POOL, QuizClient

    async def run() -> None:
        client = QuizClient(demo_mode=True)
        questions = await client.fetch_questions(10)
        assert len(questions) == 10
        assert len(DEMO_POOL) >= 10
        assert all(len(q.options) == 4 for q in questions)
        q = QuizClient._parse({
            "question": "What is H2O?",
            "correct_answer": "Water",
            "incorrect_answers": ["Fire", "Air", "Earth"],
        })
        assert q.options[q.correct_index] == "Water"
        db = Database(os.path.join(tempfile.gettempdir(), "smoke_quiz.db"))
        if os.path.exists(db.path):
            os.remove(db.path)
        await db.init()
        await db.save_result(1, "alice", 8, 10)
        await db.save_result(2, "bob", 5, 10)
        await db.save_result(1, "alice", 10, 10)
        assert (await db.leaderboard())[0] == ("alice", 10)
        assert await db.stats(1) == (2, 10)

    asyncio.run(run())
    print("  [OK] оффлайн-пул вопросов + парсинг OpenTDB + лидерборд SQLite")


def validate_p6() -> None:
    _insert("p6")
    from cbr_api import CbrClient, parse_cbr_xml
    from db import Database

    sample = """<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="05.08.2026" name="Foreign Currency Market">
<Valute ID="R01235"><NumCode>840</NumCode><CharCode>USD</CharCode><Nominal>1</Nominal>
<Name>Доллар США</Name><Value>91,2345</Value></Valute>
<Valute ID="R01820"><NumCode>392</NumCode><CharCode>JPY</CharCode><Nominal>100</Nominal>
<Name>Японская иена</Name><Value>60,8300</Value></Valute>
</ValCurs>"""
    rates = parse_cbr_xml(sample.encode("cp1251"))
    assert rates["USD"].value == 91.2345  # запятая -> точка
    assert rates["JPY"].per_one == 0.6083  # 60,83 за 100 иен

    async def run() -> None:
        client = CbrClient(demo_mode=True)
        all_rates = await client.fetch_rates()
        assert "USD" in all_rates and "EUR" in all_rates
        rub = await client.convert("USD", 100)
        assert rub is not None and rub > 0
        db = Database(os.path.join(tempfile.gettempdir(), "smoke_rates.db"))
        if os.path.exists(db.path):
            os.remove(db.path)
        await db.init()
        await db.save_rates(all_rates, "2026-08-05")
        assert len(await db.history("USD", 7)) == 1
        await db.set_digest(1, "alice", True)
        assert [u for u, _ in await db.digest_users()] == [1]

    asyncio.run(run())
    print("  [OK] парсинг XML ЦБ (байты/кодировка) + демо-курсы + история + подписка")


def validate_p7() -> None:
    """Погодный бот: демо-погода, парсеры Open-Meteo, города и рассылка."""
    _insert("p7")
    from db import Database
    from weather_api import Geocoder, WeatherClient, _parse_current, _parse_forecast

    payload = {
        "current": {
            "time": "2026-08-07T12:00", "temperature_2m": 21.5,
            "wind_speed_10m": 4.2, "relative_humidity_2m": 61, "weather_code": 2,
        },
        "daily": {
            "time": ["2026-08-07", "2026-08-08"],
            "weather_code": [2, 61],
            "temperature_2m_max": [24.0, 20.0],
            "temperature_2m_min": [15.0, 13.0],
            "precipitation_probability_max": [10, 80],
        },
    }
    cur = _parse_current(payload)
    assert cur.temperature == 21.5 and cur.code == 2
    days = _parse_forecast(payload)
    assert len(days) == 2 and days[1].precip_prob == 80.0

    async def run() -> None:
        geo = Geocoder(demo_mode=True)
        point = await geo.geocode("Москва")
        assert point is not None and point.latitude != 0
        wc = WeatherClient(demo_mode=True)
        cur_w = await wc.current(55.75, 37.62)
        assert cur_w.describe()
        fc = await wc.forecast(55.75, 37.62, days=7)
        assert len(fc) == 7
        db = Database(os.path.join(tempfile.gettempdir(), "smoke_weather.db"))
        if os.path.exists(db.path):
            os.remove(db.path)
        await db.init()
        await db.set_city(1, "alice", "Москва", 55.75, 37.62)
        await db.set_digest(1, "alice", True)
        users = await db.digest_users()
        assert users and users[0]["city"] == "Москва"

    asyncio.run(run())
    print("  [OK] demo-weather + Open-Meteo parsers + city + digest subscription")


def validate_p8() -> None:
    """Трекер расходов: парсинг /add, категории, агрегаты, экспорт CSV."""
    _insert("p8")
    from categories import parse_expense
    from db import Database

    parsed = parse_expense("500 кофе")
    assert parsed is not None and parsed[0] == 500.0 and parsed[2] == "Продукты"
    assert parse_expense("abc") is None
    assert parse_expense("0 ничего") is None

    async def run() -> None:
        db = Database(os.path.join(tempfile.gettempdir(), "smoke_expenses.db"))
        if os.path.exists(db.path):
            os.remove(db.path)
        await db.init()
        for amount, note in [(500, "кофе"), (300, "метро"), (200, "обед")]:
            await db.add_expense(1, float(amount), "Продукты" if note != "метро" else "Транспорт", note)
        from datetime import date
        today = date.today()
        assert await db.total_between(1, today, today) == 1000.0
        by_cat = await db.by_category(1, today, today)
        assert by_cat["Продукты"] == 700.0 and by_cat["Транспорт"] == 300.0
        assert len(await db.recent(1, limit=2)) == 2
        csv_path = os.path.join(tempfile.gettempdir(), "smoke_export.csv")
        count = await db.export_csv(csv_path, 1, today, today)
        assert count == 3 and os.path.getsize(csv_path) > 0

    asyncio.run(run())
    print("  [OK] auto-categorization + SQL aggregates by date + CSV export")


def validate_p9() -> None:
    """Новостной бот: RSS/Atom парсинг, дедупликация, подписки на дайджест."""
    _insert("p9")
    from db import Database
    from rss_parser import NewsItem, demo_feed, parse_feed

    rss = ("<?xml version='1.0' encoding='UTF-8'?>"
           "<rss version='2.0'><channel><title>Test</title>"
           "<item><title>Новость 1</title><link>https://x.test/1</link></item>"
           "<item><title>Новость 2</title><link>https://x.test/2</link></item>"
           "</channel></rss>").encode("utf-8")
    items = parse_feed(rss, source="Test")
    assert len(items) == 2 and items[0].title == "Новость 1"
    demo = demo_feed("Демо", amount=3)
    assert len(demo) == 3 and all(i.title for i in demo)

    async def run() -> None:
        db = Database(os.path.join(tempfile.gettempdir(), "smoke_news.db"))
        if os.path.exists(db.path):
            os.remove(db.path)
        await db.init()
        batch = [NewsItem(title="A", link="https://x/1"), NewsItem(title="B", link="https://x/2")]
        assert len(await db.save_articles(batch)) == 2
        assert await db.save_articles(batch) == []  # dedup
        assert await db.total_articles() == 2
        assert await db.subscribe(1, "https://feed.test/rss", "Test") is True
        assert await db.subscribe(1, "https://feed.test/rss", "Test") is False
        assert len(await db.all_subscriptions()) == 1

    asyncio.run(run())
    print("  [OK] RSS parsing + demo feed + dedup (UNIQUE link) + subscriptions")


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    checks = {
        "p1": validate_p1,
        "p2": validate_p2,
        "p3": validate_p3,
        "p4": validate_p4,
        "p5": validate_p5,
        "p6": validate_p6,
        "p7": validate_p7,
        "p8": validate_p8,
        "p9": validate_p9,
    }
    to_run = list(checks) if target == "all" else [target]
    for key in to_run:
        print(f"== Проект {key} ({PROJECTS[key]}) ==")
        checks[key]()
    print("=== ВАЛИДАЦИЯ ЗАВЕРШЕНА УСПЕШНО ===")


if __name__ == "__main__":
    main()
