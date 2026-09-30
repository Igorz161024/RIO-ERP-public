# frontend_rio/ui/inventory_page.py
from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.inventory import get_inventory, add_inventory_entry

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
    page.add(Table(data, columns=["id", "name", "quantity", "category"]))

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Назва товару", name="name"))
    form.add(NumberInput(label="Кількість", name="quantity"))
    form.add(TextInput(label="Категорія", name="category"))

    def on_submit(values):
        ok, msg = validate_inventory_entry(values["name"], values["quantity"], values["category"])
        if not ok:
            page.alert(msg)  # показати помилку
        else:
            add_inventory_entry(values)  # виклик сервісу
            page.toast("Запис інвентаря успішно додано")

    form.on_submit(on_submit)
    page.add(form)

    return page
