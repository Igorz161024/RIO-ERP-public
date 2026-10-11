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
    if not data:
        page.alert("ℹ️ Немає фінансових записів", type="info")
    else:
        page.add(Table(data, columns=["id", "date", "category", "amount"]))

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date", placeholder="2026-10-11"))
    form.add(TextInput(label="Категорія (income/expense/investment/loan)", name="category"))
    form.add(NumberInput(label="Сума", name="amount", placeholder="1000"))

    def on_submit(values):
        ok, msg = validate_finance_entry(values["date"], values["category"], values["amount"])
        if not ok:
            page.alert(f"❌ Помилка: {msg}", type="error")
        else:
            add_finance_entry(values)
            page.toast(
                f"✅ Запис додано: {values['category']} {values['amount']} грн",
                duration=3000
            )
            form.clear()  # очистити форму після успішного додавання

    form.on_submit(on_submit)
    page.add(form)

    return page
