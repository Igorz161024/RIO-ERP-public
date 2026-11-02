from rio import PageView, Table, AutoForm, TextInput, NumberInput

from services.accounts import (
    get_accounts,
    add_account_entry,
    delete_account_entry
)

from ui.messages import (
    show_error,
    show_info,
    show_success,
    show_warning
)


def validate_account_entry(name, balance):

    if not name.strip():
        return False, "Назва рахунку не може бути порожньою"

    if not isinstance(balance, (int, float)):
        return False, "Баланс повинен бути числом"

    return True, "OK"


def accounts_page(page: PageView):

    data = get_accounts()

    if not data:
        show_info(page, "Немає бухгалтерських рахунків")

    else:

        table = Table(
            data,
            columns=[
                "id",
                "name",
                "balance"
            ],
            actions=[
                {
                    "label": "Видалити",
                    "name": "delete_account"
                }
            ]
        )

        def on_action(action, row):

            if action == "delete_account":

                show_warning(
                    page,
                    f"Ви дійсно хочете видалити рахунок '{row['name']}'?"
                )

                try:

                    delete_account_entry(row["id"])

                    show_success(
                        page,
                        "Рахунок успішно видалено"
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
            label="Назва рахунку",
            name="name"
        )
    )

    form.add(
        NumberInput(
            label="Початковий баланс",
            name="balance",
            placeholder="0"
        )
    )

    def on_submit(values):

        ok, msg = validate_account_entry(
            values["name"],
            values["balance"]
        )

        if not ok:

            show_error(page, msg)

        else:

            try:

                add_account_entry(values)

                show_success(
                    page,
                    "Рахунок успішно додано"
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