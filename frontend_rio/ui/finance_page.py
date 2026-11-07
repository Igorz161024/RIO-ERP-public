import rio

from services.finance import get_finance


@rio.page(
    name="Finance",
    url_segment="finance"
)
class FinancePage(rio.Component):

    def build(self) -> rio.Component:

        entries = get_finance()

        rows = [
            rio.Text(
                "ID | Date | Account | Debit | Credit | Balance",
                style="heading3"
            ),
            rio.Text(
                "[ Refresh ] [ Add Entry ] [ Edit Entry ] [ Delete Entry ]"
            ),
            rio.Text(
                "-" * 70
            ),
        ]

        for entry in entries:

            rows.append(
                rio.Text(
                    f"{entry['id']} | "
                    f"{entry['date']} | "
                    f"{entry['account']} | "
                    f"{entry['debit']} | "
                    f"{entry['credit']} | "
                    f"{entry['balance']}"
                )
            )

        return rio.Column(
            rio.Text(
                "Finance",
                style="heading2"
            ),
            rio.Text(
                f"Records: {len(entries)}"
            ),
            rio.Text(
                "Finance API Connected",
                style="heading3"
            ),
            *rows,
            spacing=0.5,
            margin=2,
        )