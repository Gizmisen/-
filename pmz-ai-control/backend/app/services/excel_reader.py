from pathlib import Path

import pandas as pd


CSV_SHEET = "csv"


def load_sheet(path: Path, sheet_name: str | None = None) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if not sheet_name:
        raise ValueError("sheet_name is required for Excel files")
    return pd.read_excel(path, sheet_name=sheet_name)


def read_file_preview(path: Path, max_rows: int = 20) -> dict:
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
        return {
            "sheet_names": [CSV_SHEET],
            "columns": {CSV_SHEET: [str(c) for c in df.columns]},
            "preview": {CSV_SHEET: df.head(max_rows).fillna("").to_dict(orient="records")},
        }

    xls = pd.ExcelFile(path)
    sheets: dict[str, list[dict]] = {}
    columns: dict[str, list[str]] = {}
    for sheet in xls.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet)
        columns[sheet] = [str(c) for c in df.columns]
        sheets[sheet] = df.head(max_rows).fillna("").to_dict(orient="records")
    return {"sheet_names": xls.sheet_names, "columns": columns, "preview": sheets}
