import rio

from services.sales import get_sales


@rio.page(
    name="Sales",
    url_segment="sales"
)
class SalesPage(rio.Component):

    def build(self) -> rio.Component:

        entries = get_sales()

        rows = [
            rio.Text(
                "ID | Client | Product | Qty | Price | Amount",
                style="heading3"
            ),
            rio.Text(
                "[ Refresh ] [ Add Sale ] [ Edit Sale ] [ Delete Sale ]"
            ),
            rio.Text(
                "-" * 80
            ),
        ]

        for entry in entries:
            rows.append(
                rio.Text(
                    f"{entry['id']} | "
                    f"{entry['client']} | "
                    f"{entry['product']} | "
                    f"{entry['quantity']} | "
                    f"{entry['price']} | "
                    f"{entry['amount']}"
                )
            )

        return rio.Column(
            rio.Text(
                "Sales",
                style="heading2"
            ),
            rio.Text(
                f"Records: {len(entries)}"
            ),
            rio.Text(
                "Sales API Connected",
                style="heading3"
            ),
            *rows,
            spacing=0.5,
            margin=2,
        )