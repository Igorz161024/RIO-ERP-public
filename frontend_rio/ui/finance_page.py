# frontend_rio/ui/finance_page.py
from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.finance import get_finance, add_finance_entry
import datetime

# 🔹 Допустимі категорії витрат/доходів
ALLOWED_CATEGORIES = ["income", "expense", "investment", "loan"]

# 🔹 Допоміжна функція для перевірки введених даних
def validate_finance_entry(date, category, amount):
    if not date.strip():
        return False, "Дата не може бути порожньою"
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False, "Невірний формат дати (YYYY-MM-DD)"

    if category not in ALLOWED_CATEGORIES:
        return False, f"Недопустима категорія. Дозволені: {', '.join(ALLOWED_CATEGORIES)}"

    if not isinstance(amount, (int, float)):
        return False, "Сума має бути числом"
    if amount <= 0:
        return False, "Сума має бути > 0"

    return True, "OK"

# 🔹 Основна функція сторінки
def finance_page(page: PageView):
    # показ таблиці з бекенду
    data = get_finance()
    page.add(Table(data, columns=["id", "date", "category", "amount"]))

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date"))
    form.add(TextInput(label="Категорія", name="category"))
    form.add(NumberInput(label="Сума", name="amount"))

    def on_submit(values):
        ok, msg = validate_finance_entry(values["date"], values["category"], values["amount"])
        if not ok:
            page.alert(msg)  # показати помилку
        else:
            add_finance_entry(values)  # виклик сервісу
            page.toast("Фінансовий запис успішно додано")

    form.on_submit(on_submit)
    page.add(form)

    return page
