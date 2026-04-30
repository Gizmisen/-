import json
import os
from datetime import date

from sqlalchemy.orm import Session

from app.models.orders import Order
from app.models.production_fact import ProductionFact
from app.models.production_plan import ProductionPlan
from app.services.ai_analysis_service import find_fact_without_plan, find_plan_without_fact, find_portfolio_without_plan, find_warehouse_shortages
from app.services.dashboard_service import build_dashboard
from app.services.plan_fact_service import build_plan_fact_report


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def find_order(db: Session, order_number: str) -> dict | None:
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        return None
    return {
        "order_number": order.order_number,
        "status": order.status,
        "plant": order.plant,
        "quantity": float(order.quantity or 0),
        "required_date": str(order.required_date) if order.required_date else None,
    }


def find_material_usage(db: Session, material_code: str) -> dict:
    plan_count = db.query(ProductionPlan).filter(ProductionPlan.material_code == material_code).count()
    fact_count = db.query(ProductionFact).filter(ProductionFact.material_code == material_code).count()
    return {"material_code": material_code, "plan_rows": plan_count, "fact_rows": fact_count}


def analyze_plan_fact(db: Session, period: str | None = None, status: str | None = None, limit: int = 50) -> list[dict]:
    items = build_plan_fact_report(db, period=period)
    if status:
        items = [x for x in items if x.get("status") == status]
    return items[:limit]


def get_overdue_items(db: Session, today: str | None = None) -> list[dict]:
    today_date = date.fromisoformat(today) if today else date.today()
    rows = []
    for o in db.query(Order).all():
        if o.required_date and o.required_date < today_date and (o.status or "") != "closed":
            rows.append({"order_number": o.order_number, "required_date": str(o.required_date), "status": o.status})
    return rows


def _local_answer(db: Session, query: str) -> tuple[str, dict | list | None]:
    q = query.lower()
    if "заказ" in q:
        number = "".join(ch for ch in query if ch.isdigit())
        if number:
            data = find_order(db, number)
            if data:
                return f"Заказ {number} найден. Статус: {data.get('status') or 'не указан'}.", data
            return f"Заказ {number} не найден.", None

    if "материал" in q:
        token = query.strip().split()[-1]
        data = find_material_usage(db, token)
        return f"Материал {token}: плановых строк {data['plan_rows']}, фактических строк {data['fact_rows']}.", data

    if "план" in q and "факт" in q:
        period = next((part for part in query.split() if len(part) == 7 and part[4] == "-"), None)
        issues = analyze_plan_fact(db, period=period)
        return f"Найдено {len(issues)} позиций в отчете план-факт.", issues

    if "просроч" in q:
        overdue = get_overdue_items(db)
        return f"Просроченных заказов: {len(overdue)}", overdue


    if "свод" in q or "dashboard" in q or "контур" in q:
        data = build_dashboard(db)
        return (
            "Сводка контура: "
            f"портфель={data['portfolio_rows']}, план={data['planning_rows']}, факт={data['fact_rows']}, "
            f"труд={data['labor_fact_rows']}, сбыт={data['sales_orders']}, склад={data['warehouse_rows']}, sap={data['sap_orders']}.",
            data,
        )

    return (
        "Я умею: искать заказ, анализировать план-факт, просрочки и материал. "
        "Пример: 'Покажи план-факт 2026-03 статус нет факта'",
        None,
    )


def _tool_schema() -> list[dict]:
    return [
        {"type": "function", "function": {"name": "find_order", "description": "Find order by order number", "parameters": {"type": "object", "properties": {"order_number": {"type": "string"}}, "required": ["order_number"]}}},
        {"type": "function", "function": {"name": "find_material_usage", "description": "Find material usage in plan/fact", "parameters": {"type": "object", "properties": {"material_code": {"type": "string"}}, "required": ["material_code"]}}},
        {"type": "function", "function": {"name": "analyze_plan_fact", "description": "Analyze plan/fact report", "parameters": {"type": "object", "properties": {"period": {"type": "string"}, "status": {"type": "string"}, "limit": {"type": "integer"}}}}},
        {"type": "function", "function": {"name": "get_overdue_items", "description": "Get overdue items", "parameters": {"type": "object", "properties": {"today": {"type": "string"}}}}},
        {"type": "function", "function": {"name": "find_plan_without_fact", "description": "Find planned rows without fact", "parameters": {"type": "object", "properties": {"period": {"type": "string"}, "limit": {"type": "integer"}}}}},
        {"type": "function", "function": {"name": "find_fact_without_plan", "description": "Find fact rows without plan", "parameters": {"type": "object", "properties": {"period": {"type": "string"}, "limit": {"type": "integer"}}}}},
        {"type": "function", "function": {"name": "find_portfolio_without_plan", "description": "Find portfolio rows without plan", "parameters": {"type": "object", "properties": {"limit": {"type": "integer"}}}}},
        {"type": "function", "function": {"name": "find_warehouse_shortages", "description": "Find warehouse shortages", "parameters": {"type": "object", "properties": {"limit": {"type": "integer"}}}}},
    ]


def _execute_tool(db: Session, name: str, arguments: dict):
    if name == "find_order":
        return find_order(db, arguments["order_number"])
    if name == "find_material_usage":
        return find_material_usage(db, arguments["material_code"])
    if name == "analyze_plan_fact":
        return analyze_plan_fact(db, period=arguments.get("period"), status=arguments.get("status"), limit=arguments.get("limit", 50))
    if name == "get_overdue_items":
        return get_overdue_items(db, today=arguments.get("today"))
    if name == "find_plan_without_fact":
        return find_plan_without_fact(db, period=arguments.get("period"), limit=arguments.get("limit", 200))
    if name == "find_fact_without_plan":
        return find_fact_without_plan(db, period=arguments.get("period"), limit=arguments.get("limit", 200))
    if name == "find_portfolio_without_plan":
        return find_portfolio_without_plan(db, limit=arguments.get("limit", 200))
    if name == "find_warehouse_shortages":
        return find_warehouse_shortages(db, limit=arguments.get("limit", 200))
    return {"error": f"Unknown tool {name}"}


def answer_query(db: Session, query: str, advanced: bool = True) -> tuple[str, dict | list | None, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not advanced or not api_key:
        answer, data = _local_answer(db, query)
        return answer, data, "local"

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        messages = [
            {"role": "system", "content": "You are PMZ production assistant. Use tools when needed. Never invent DB facts."},
            {"role": "user", "content": query},
        ]

        first = client.chat.completions.create(model=OPENAI_MODEL, messages=messages, tools=_tool_schema(), tool_choice="auto")
        msg = first.choices[0].message

        if msg.tool_calls:
            tool_payload = []
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments or "{}")
                result = _execute_tool(db, tc.function.name, args)
                tool_payload.append({"tool": tc.function.name, "result": result})
                messages.append({"role": "assistant", "tool_calls": [tc.model_dump()]})
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result, ensure_ascii=False)})

            second = client.chat.completions.create(model=OPENAI_MODEL, messages=messages)
            final = second.choices[0].message.content or "Готово"
            return final, tool_payload, "openai"

        return msg.content or "Готово", None, "openai"
    except Exception:
        answer, data = _local_answer(db, query)
        return answer, data, "local_fallback"
