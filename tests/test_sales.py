import pytest
from frontend_rio.ui.sales_page import validate_sale_entry

def test_validate_sale_entry_valid():
    ok, msg = validate_sale_entry("2026-10-12", "Іван", 1000, "completed")
    assert ok is True
    assert msg == "OK"

def test_validate_sale_entry_empty_date():
    ok, msg = validate_sale_entry("", "Іван", 1000, "completed")
    assert ok is False
    assert "Дата не може бути порожньою" in msg

def test_validate_sale_entry_invalid_date_format():
    ok, msg = validate_sale_entry("12-10-2026", "Іван", 1000, "completed")
    assert ok is False
    assert "Невірний формат дати" in msg

def test_validate_sale_entry_invalid_amount():
    ok, msg = validate_sale_entry("2026-10-12", "Іван", -50, "completed")
    assert ok is False
    assert "Сума має бути числом > 0" in msg

def test_validate_sale_entry_invalid_status():
    ok, msg = validate_sale_entry("2026-10-12", "Іван", 1000, "wrong_status")
    assert ok is False
    assert "Недопустимий статус" in msg
