from rio import PageView, Table, AutoForm, TextInput, NumberInput
from frontend_rio.services.sales import get_sales, add_sales_entry, delete_sales_entry
from frontend_rio.ui.messages import show_error, show_info, show_success, show_warning
import datetime

# 🔹 Допустимі статуси продажу
ALLOWED_STATUSES = ["pending", "completed", "canceled"]

# 🔹 Допоміжна функція для перевірки введених даних
def validate_sale_entry(date, customer, amount, status):
    if not date.strip():
        return False, "Дата не може бути порожньою"
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False, "Невірний формат дати (YYYY-MM-DD)"

    if not customer.strip():
        return False, "Клієнт не може бути порожнім"

    if not isinstance(amount, (int, float)) or amount <= 0:
        return False, "Сума має бути числом > 0"

    if status not in ALLOWED_STATUSES:
        return False, f"Недопустимий статус. Дозволені: {', '.join(ALLOWED_STATUSES)}"

    return True, "OK"

# 🔹 Основна функція сторінки
def sales_page(page: PageView):
    # показ таблиці з бекенду
    data = get_sales()
    if not data:
        show_info(page, "Немає записів продажів")
    else:
        table = Table(
            data,
            columns=["id", "date", "customer", "amount", "status"],
            actions=[{"label": "Видалити", "name": "delete_sale"}]
        )

        # обробка дій у таблиці
        def on_action(action, row):
            if action == "delete_sale":
                show_warning(page, f"Ви дійсно хочете видалити продаж №{row['id']}?")
                try:
                    delete_sales_entry(row["id"])
                    show_success(page, "Продаж успішно видалено")
                except Exception as e:
                    show_error(page, f"Помилка при видаленні: {str(e)}")

        table.on_action(on_action)
        page.add(table)

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date", placeholder="2026-10-11"))
    form.add(TextInput(label="Клієнт", name="customer"))
    form.add(NumberInput(label="Сума", name="amount", placeholder="1000"))
    form.add(TextInput(label="Статус (pending/completed/canceled)", name="status"))

    def on_submit(values):
        ok, msg = validate_sale_entry(values["date"], values["customer"], values["amount"], values["status"])
        if not ok:
            show_error(page, msg)
        else:
            try:
                add_sales_entry(values)
                show_success(page, "Продаж успішно додано")
                form.clear()  # очистити форму після успішного додавання
            except Exception as e:
                show_error(page, f"Помилка при додаванні: {str(e)}")

    form.on_submit(on_submit)
    page.add(form)

    return page
