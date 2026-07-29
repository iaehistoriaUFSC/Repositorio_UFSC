from app.chronology import period_for_year


def test_requested_period_boundaries_are_unambiguous():
    assert period_for_year(1600)["id"] == "A"
    assert period_for_year(1749)["id"] == "A"
    assert period_for_year(1750)["id"] == "B"
    assert period_for_year(1849)["id"] == "B"
    assert period_for_year(1850)["id"] == "C"
    assert period_for_year(1945)["id"] == "C"
    assert period_for_year(1946)["id"] == "transition-1946-1949"
    assert period_for_year(1949)["id"] == "transition-1946-1949"
    assert period_for_year(1950)["id"] == "D"


def test_missing_and_pre_1600_dates_are_not_silently_forced():
    assert period_for_year(None)["status"] == "missing_document_year"
    assert period_for_year(1599)["status"] == "outside_requested_periodization"

