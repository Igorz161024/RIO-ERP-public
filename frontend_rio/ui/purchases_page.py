import rio

from services.purchases import get_purchases


@rio.page(
    name="Purchases",
    url_segment="purchases"
)
class PurchasesPage(rio.Component):

    def build(self) -> rio.Component:

        entries = get_purchases()

        rows = [
            rio.Text(
                "ID | Supplier | Country | Product | Qty | Price | Amount",
                style="heading3"
            ),
            rio.Text(
                "[ Refresh ] [ Add Purchase ] [ Edit Purchase ] [ Delete Purchase ]"
            ),
            rio.Text(
                "-" * 90
            ),
        ]

        for entry in entries:
            rows.append(
                rio.Text(
                    f"{entry['id']} | "
                    f"{entry['supplier']} | "
                    f"{entry['country']} | "
                    f"{entry['product']} | "
                    f"{entry['quantity']} | "
                    f"{entry['price']} | "
                    f"{entry['amount']}"
                )
            )

        return rio.Column(
            rio.Text(
                "Purchases",
                style="heading2"
            ),
            rio.Text(
                f"Records: {len(entries)}"
            ),
            rio.Text(
                "Purchases API Connected",
                style="heading3"
            ),
            *rows,
            spacing=0.5,
            margin=2,
        )