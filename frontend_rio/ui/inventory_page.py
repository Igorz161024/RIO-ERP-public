from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.inventory import (
    get_inventory,
    add_inventory_entry,
    delete_inventory_entry
)
from ui.messages import (
    show_error,
    show_info,
    show_success,
    show_warning
)


# Перевірка введених даних
def validate_inventory_entry(product, quantity, batch, price):

    if not product.strip():
        return False, "Назва товару не може бути порожньою"

    if not isinstance(quantity, int) or quantity <= 0:
        return False, "Кількість повинна бути більше 0"

    if not batch.strip():
        return False, "Партія не може бути порожньою"

    if not isinstance(price, (int, float)) or price <= 0:
        return False, "Ціна повинна бути більше 0"

    return True, "OK"


# Основна сторінка
def inventory_page(page: PageView):

    data = get_inventory()

    if not data:
        show_info(page, "Немає записів інвентаря")

    else:

        table = Table(
            data,
            columns=[
                "id",
                "product",
                "quantity",
                "batch",
                "price"
            ],
            actions=[
                {
                    "label": "Видалити",
                    "name": "delete_inventory"
                }
            ]
        )

        def on_action(action, row):

            if action == "delete_inventory":

                show_warning(
                    page,
                    f"Ви дійсно хочете видалити товар '{row['product']}'?"
                )

                try:
                    delete_inventory_entry(row["id"])

                    show_success(
                        page,
                        "Товар успішно видалено"
                    )

                except Exception as e:
                    show_error(
                        page,
                        f"Помилка при видаленні: {str(e)}"
                    )

        table.on_action(on_action)

        page.add(table)

    form = AutoForm()

    form.add(
        TextInput(
            label="Назва товару",
            name="product"
        )
    )

    form.add(
        NumberInput(
            label="Кількість",
            name="quantity",
            placeholder="10"
        )
    )

    form.add(
        TextInput(
            label="Партія",
            name="batch",
            placeholder="BATCH-001"
        )
    )

    form.add(
        NumberInput(
            label="Ціна",
            name="price",
            placeholder="100.00"
        )
    )

    def on_submit(values):

        ok, msg = validate_inventory_entry(
            values["product"],
            values["quantity"],
            values["batch"],
            values["price"]
        )

        if not ok:

            show_error(page, msg)

        else:

            try:

                add_inventory_entry(values)

                show_success(
                    page,
                    "Товар успішно додано на склад"
                )

                form.clear()

            except Exception as e:

                show_error(
                    page,
                    f"Помилка при додаванні: {str(e)}"
                )

    form.on_submit(on_submit)

    page.add(form)

    return page