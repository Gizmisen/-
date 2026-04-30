from pathlib import Path

from app.services.excel_reader import read_file_preview


def analyze_excel_file(path: Path) -> dict:
    preview = read_file_preview(path, max_rows=5)
    sheets = preview.get("sheet_names", [])
    recommendations = {}
    for s in sheets:
        low = s.lower()
        if "план" in low:
            recommendations[s] = "plan"
        elif "fact" in low or "coois" in low or "факт" in low:
            recommendations[s] = "fact"
        elif "издел" in low or "тех" in low or "спец" in low:
            recommendations[s] = "production-data"
        elif "портф" in low or "заголов" in low:
            recommendations[s] = "portfolio"
        elif "сз" in low or "потреб" in low or "график" in low:
            recommendations[s] = "orders-history"
        else:
            recommendations[s] = "unknown"
    return {"sheet_names": sheets, "preview": preview.get("rows", [])[:5], "recommendations": recommendations}
