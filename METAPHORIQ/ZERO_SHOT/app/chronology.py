from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Period:
    id: str
    label: str
    start: int | None
    end: int | None
    status: str = "defined"


PERIODS = (
    Period("A", "A · 1600–1749", 1600, 1749),
    Period("B", "B · 1750–1849", 1750, 1849),
    Period("C", "C · 1850–1945", 1850, 1945),
    Period(
        "transition-1946-1949",
        "Transition · 1946–1949",
        1946,
        1949,
        "gap_in_requested_periodization",
    ),
    Period("D", "D · 1950 onwards", 1950, None),
)


def period_for_year(year: int | None) -> dict:
    if year is None:
        return {
            "id": "unresolved",
            "label": "Unresolved date",
            "start": None,
            "end": None,
            "status": "missing_document_year",
        }
    if year < 1600:
        return {
            "id": "pre-1600",
            "label": "Before requested chronology",
            "start": None,
            "end": 1599,
            "status": "outside_requested_periodization",
        }
    for period in PERIODS:
        if year >= (period.start or year) and (
            period.end is None or year <= period.end
        ):
            return asdict(period)
    raise AssertionError(f"unhandled year: {year}")

