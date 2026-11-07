import rio

from services.accounts import get_accounts


@rio.page(
    name="Accounts",
    url_segment="accounts"
)
class AccountsPage(rio.Component):

    def build(self) -> rio.Component:

        accounts = get_accounts()

        rows = [
            rio.Text(
                "ID | Name | Balance",
                style="heading3"
            ),
            rio.Text(
                "[ Refresh ] [ Add Account ] [ Edit Account ] [ Delete Account ]"
            ),
            rio.Text(
                "-" * 50
            ),
        ]

        for account in accounts:
            rows.append(
                rio.Text(
                    f"{account['id']} | "
                    f"{account['name']} | "
                    f"{account['balance']}"
                )
            )

        return rio.Column(
            rio.Text(
                "Accounts",
                style="heading2"
            ),
            rio.Text(
                f"Records: {len(accounts)}"
            ),
            rio.Text(
                "Accounts API Connected",
                style="heading3"
            ),
            *rows,
            spacing=0.5,
            margin=2,
        )