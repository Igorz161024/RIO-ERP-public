# frontend_rio/ui/journal_page.py
from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.journal import get_journal, add_journal_entry
import datetime

# 🔹 Допоміжна функція для перевірки введених даних
def validate_journal_entry(date, operation, amount, status):
    if not date.strip():
        return False, "Дата не може бути порожньою"
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False, "Невірний формат дати (YYYY-MM-DD)"

    if not operation.strip():
        return False, "Операція не може бути порожньою"

    if not isinstance(amount, (int, float)) or amount <= 0:
        return False, "Сума має бути числом > 0"

    if not status.strip():
        return False, "Статус не може бути порожнім"

    return True, "OK"

# 🔹 Основна функція сторінки
def journal_page(page: PageView):
    # показ таблиці з бекенду
    data = get_journal()
    page.add(Table(data, columns=["id", "date", "operation", "status", "amount"]))

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date"))
    form.add(TextInput(label="Операція", name="operation"))
    form.add(NumberInput(label="Сума", name="amount"))
    form.add(TextInput(label="Статус", name="status"))

    def on_submit(values):
        ok, msg = validate_journal_entry(values["date"], values["operation"], values["amount"], values["status"])
        if not ok:
            page.alert(msg)  # показати помилку
        else:
            add_journal_entry(values)  # виклик сервісу
            page.toast("Запис у журнал успішно додано")

    form.on_submit(on_submit)
    page.add(form)

    return page
