# src/tools/exporter_tool.py

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


def export_json(path: str, data: Any) -> None:
    """
    Write data to a JSON file with pretty formatting.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def export_csv(path: str, rows: Iterable[Mapping[str, Any]]) -> None:
    """
    Write an iterable of dict-like rows to a CSV file.

    :param path: Output file path.
    :param rows: Iterable of dictionaries with consistent keys.
    """
    rows = list(rows)
    if not rows:
        # nothing to write
        return

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())

    with p.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


# Placeholder for future email / external exports
def send_email_report(to_address: str, subject: str, body: str) -> None:
    """
    Stubbed email sender. In a real system, you would integrate with
    an SMTP server or an email API provider.
    """
    # For now, just log or print.
    print(f"[EMAIL → {to_address}] {subject}\n{body}\n")
