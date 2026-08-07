"""Валидация проектов. Запускать ПО ОДНОМУ ПРОЕКТУ на процесс:
    .venv/Scripts/python _validate.py p1|p2|p3|p4

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


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    checks = {
        "p1": validate_p1,
        "p2": validate_p2,
        "p3": validate_p3,
        "p4": validate_p4,
        "p5": validate_p5,
        "p6": validate_p6,
    }
    to_run = list(checks) if target == "all" else [target]
    for key in to_run:
        print(f"== Проект {key} ({PROJECTS[key]}) ==")
        checks[key]()
    print("=== ВАЛИДАЦИЯ ЗАВЕРШЕНА УСПЕШНО ===")


if __name__ == "__main__":
    main()
