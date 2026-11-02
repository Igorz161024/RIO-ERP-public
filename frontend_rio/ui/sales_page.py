from rio import PageView, Table, AutoForm, TextInput, NumberInput

from services.sales import (
    get_sales,
    add_sales_entry,
    delete_sales_entry
)

from ui.messages import (
    show_error,
    show_info,
    show_success,
    show_warning
)


def validate_sale_entry(
    client,
    product,
    quantity,
    price
):
    if not client.strip():
        return False, "Клієнт не може бути порожнім"

    if not product.strip():
        return False, "Товар не може бути порожнім"

    if quantity <= 0:
        return False, "Кількість повинна бути більше 0"

    if price <= 0:
        return False, "Ціна повинна бути більше 0"

    return True, "OK"


def sales_page(page: PageView):

    data = get_sales()

    if not data:
        show_info(page, "Немає записів продажів")

    else:

        table = Table(
            data,
            columns=[
                "id",
                "client",
                "product",
                "quantity",
                "price",
                "amount"
            ],
            actions=[
                {
                    "label": "Видалити",
                    "name": "delete_sale"
                }
            ]
        )

        def on_action(action, row):

            if action == "delete_sale":

                show_warning(
                    page,
                    f"Видалити продаж клієнта '{row['client']}'?"
                )

                try:

                    delete_sales_entry(row["id"])

                    show_success(
                        page,
                        "Продаж успішно видалено"
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
            label="Клієнт",
            name="client"
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

        ok, msg = validate_sale_entry(
            values["client"],
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

                add_sales_entry(values)

                show_success(
                    page,
                    "Продаж успішно додано"
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
