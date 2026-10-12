from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.finance import get_finance, add_finance_entry, delete_finance_entry
from ui.messages import show_error, show_info, show_success, show_warning
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
        show_info(page, "Немає фінансових записів")
    else:
        table = Table(
            data,
            columns=["id", "date", "category", "amount"],
            actions=[{"label": "Видалити", "name": "delete_finance"}]
        )

        # обробка дій у таблиці
        def on_action(action, row):
            if action == "delete_finance":
                show_warning(page, f"Ви дійсно хочете видалити запис {row['id']}?")
                try:
                    delete_finance_entry(row["id"])
                    show_success(page, "Фінансовий запис успішно видалено")
                except Exception as e:
                    show_error(page, f"Помилка при видаленні: {str(e)}")

        table.on_action(on_action)
        page.add(table)

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date", placeholder="2026-10-11"))
    form.add(TextInput(label="Категорія (income/expense/investment/loan)", name="category"))
    form.add(NumberInput(label="Сума", name="amount", placeholder="1000"))

    def on_submit(values):
        ok, msg = validate_finance_entry(values["date"], values["category"], values["amount"])
        if not ok:
            show_error(page, msg)
        else:
            try:
                add_finance_entry(values)
                show_success(page, f"Запис додано: {values['category']} {values['amount']} грн")
                form.clear()  # очистити форму після успішного додавання
            except Exception as e:
                show_error(page, f"Помилка при додаванні: {str(e)}")

    form.on_submit(on_submit)
    page.add(form)

    return page
