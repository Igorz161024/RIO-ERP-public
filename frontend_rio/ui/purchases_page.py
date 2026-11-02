from rio import PageView, Table, AutoForm, TextInput, NumberInput

from services.purchases import (
    get_purchases,
    add_purchase_entry,
    delete_purchase_entry
)

from ui.messages import (
    show_error,
    show_info,
    show_success,
    show_warning
)


def validate_purchase_entry(
    supplier,
    country,
    product,
    quantity,
    price
):
    if not supplier.strip():
        return False, "Постачальник не може бути порожнім"

    if not country.strip():
        return False, "Країна не може бути порожньою"

    if not product.strip():
        return False, "Товар не може бути порожнім"

    if quantity <= 0:
        return False, "Кількість повинна бути більше 0"

    if price <= 0:
        return False, "Ціна повинна бути більше 0"

    return True, "OK"


def purchases_page(page: PageView):

    data = get_purchases()

    if not data:
        show_info(page, "Немає записів закупівель")

    else:

        table = Table(
            data,
            columns=[
                "id",
                "supplier",
                "country",
                "product",
                "quantity",
                "price",
                "amount"
            ],
            actions=[
                {
                    "label": "Видалити",
                    "name": "delete_purchase"
                }
            ]
        )

        def on_action(action, row):

            if action == "delete_purchase":

                show_warning(
                    page,
                    f"Видалити закупівлю від постачальника '{row['supplier']}'?"
                )

                try:

                    delete_purchase_entry(row["id"])

                    show_success(
                        page,
                        "Закупівлю успішно видалено"
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
            label="Постачальник",
            name="supplier"
        )
    )

    form.add(
        TextInput(
            label="Країна",
            name="country"
        )
    )

    form.add(
        TextInput(
            label="Товар",
            name="product"
        )
    )

    form.add(
        NumberInput(
            label="Кількість",
            name="quantity",
            placeholder="1"
        )
    )

    form.add(
        NumberInput(
            label="Ціна",
            name="price",
            placeholder="100"
        )
    )

    def on_submit(values):

        ok, msg = validate_purchase_entry(
            values["supplier"],
            values["country"],
            values["product"],
            values["quantity"],
            values["price"]
        )

        if not ok:

            show_error(page, msg)

        else:

            try:

                values["amount"] = (
                    float(values["quantity"])
                    * float(values["price"])
                )

                add_purchase_entry(values)

                show_success(
                    page,
                    "Закупівлю успішно додано"
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
