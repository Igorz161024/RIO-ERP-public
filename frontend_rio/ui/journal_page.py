import rio

from services.journal import get_journal


@rio.page(
    name="Journal",
    url_segment=""
)
class JournalPage(rio.Component):

    def build(self) -> rio.Component:

        entries = get_journal()

        rows = [
            rio.Text(
                "ID | Date | Operation | Status | Amount | Account",
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
                    f"{entry['operation']} | "
                    f"{entry['status']} | "
                    f"{entry['amount']} | "
                    f"{entry['account_id']}"
                )
            )

        return rio.Column(
            rio.Text(
                "Journal",
                style="heading2"
            ),
            rio.Text(
                f"Records: {len(entries)}"
            ),
            rio.Text(
                "Journal API Connected",
                style="heading3"
            ),
            *rows,
            spacing=0.5,
            margin=2,
        )