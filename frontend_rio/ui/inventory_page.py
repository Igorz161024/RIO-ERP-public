from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.inventory import get_inventory, add_inventory_entry, delete_inventory_entry
from ui.messages import show_error, show_info, show_success, show_warning

# 🔹 Допоміжна функція для перевірки введених даних
def validate_inventory_entry(name, quantity, category):
    if not name.strip():
        return False, "Назва товару не може бути порожньою"

    if not isinstance(quantity, int) or quantity <= 0:
        return False, "Кількість має бути цілим числом > 0"

    if not category.strip():
        return False, "Категорія не може бути порожньою"

    return True, "OK"

# 🔹 Основна функція сторінки
def inventory_page(page: PageView):
    # показ таблиці з бекенду
    data = get_inventory()
    if not data:
        show_info(page, "Немає записів інвентаря")
    else:
        table = Table(
            data,
            columns=["id", "name", "quantity", "category"],
            actions=[{"label": "Видалити", "name": "delete_inventory"}]
        )

        # обробка дій у таблиці
        def on_action(action, row):
            if action == "delete_inventory":
                show_warning(page, f"Ви дійсно хочете видалити товар '{row['name']}'?")
                try:
                    delete_inventory_entry(row["id"])
                    show_success(page, "Запис інвентаря успішно видалено")
                except Exception as e:
                    show_error(page, f"Помилка при видаленні: {str(e)}")

        table.on_action(on_action)
        page.add(table)

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Назва товару", name="name"))
    form.add(NumberInput(label="Кількість", name="quantity", placeholder="10"))
    form.add(TextInput(label="Категорія", name="category"))

    def on_submit(values):
        ok, msg = validate_inventory_entry(values["name"], values["quantity"], values["category"])
        if not ok:
            show_error(page, msg)
        else:
            try:
                add_inventory_entry(values)
                show_success(page, "Запис інвентаря успішно додано")
                form.clear()  # очистити форму після успішного додавання
            except Exception as e:
                show_error(page, f"Помилка при додаванні: {str(e)}")

    form.on_submit(on_submit)
    page.add(form)

    return page

