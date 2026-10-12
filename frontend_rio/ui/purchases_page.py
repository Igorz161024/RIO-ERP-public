from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.purchases import get_purchases, add_purchase_entry, delete_purchase_entry
from ui.messages import show_error, show_info, show_success, show_warning
import datetime

# 🔹 Допоміжна функція для перевірки введених даних
def validate_purchase_entry(date, supplier, item, amount):
    if not date.strip():
        return False, "Дата не може бути порожньою"
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False, "Невірний формат дати (YYYY-MM-DD)"

    if not supplier.strip():
        return False, "Постачальник не може бути порожнім"

    if not item.strip():
        return False, "Назва товару не може бути порожньою"

    if not isinstance(amount, (int, float)) or amount <= 0:
        return False, "Сума має бути числом > 0"

    return True, "OK"

# 🔹 Основна функція сторінки
def purchases_page(page: PageView):
    # показ таблиці з бекенду
    data = get_purchases()
    if not data:
        show_info(page, "Немає записів закупівель")
    else:
        table = Table(
            data,
            columns=["id", "date", "supplier", "item", "amount"],
            actions=[{"label": "Видалити", "name": "delete_purchase"}]
        )

        # обробка дій у таблиці
        def on_action(action, row):
            if action == "delete_purchase":
                show_warning(page, f"Ви дійсно хочете видалити закупівлю №{row['id']}?")
                try:
                    delete_purchase_entry(row["id"])
                    show_success(page, "Закупівлю успішно видалено")
                except Exception as e:
                    show_error(page, f"Помилка при видаленні: {str(e)}")

        table.on_action(on_action)
        page.add(table)

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date", placeholder="2026-10-11"))
    form.add(TextInput(label="Постачальник", name="supplier"))
    form.add(TextInput(label="Назва товару", name="item"))
    form.add(NumberInput(label="Сума", name="amount", placeholder="1000"))

    def on_submit(values):
        ok, msg = validate_purchase_entry(values["date"], values["supplier"], values["item"], values["amount"])
        if not ok:
            show_error(page, msg)
        else:
            try:
                add_purchase_entry(values)
                show_success(page, "Закупівлю успішно додано")
                form.clear()  # очистити форму після успішного додавання
            except Exception as e:
                show_error(page, f"Помилка при додаванні: {str(e)}")

    form.on_submit(on_submit)
    page.add(form)

    return page
