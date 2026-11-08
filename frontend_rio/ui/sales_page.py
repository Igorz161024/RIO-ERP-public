import rio

from services.sales import get_sales


@rio.page(
    name="Sales",
    url_segment="sales"
)
class SalesPage(rio.Component):

    def build(self) -> rio.Component:

        entries = get_sales()

        rows = []

        for entry in entries:
            rows.append(
                rio.Column(
                    rio.Text(
                        f"ID: {entry['id']}"
                    ),
                    rio.Text(
                        f"Client: {entry['client']}"
                    ),
                    rio.Text(
                        f"Product: {entry['product']}"
                    ),
                    rio.Text(
                        f"Quantity: {entry['quantity']}"
                    ),
                    rio.Text(
                        f"Price: {entry['price']}"
                    ),
                    rio.Text(
                        f"Amount: {entry['amount']}"
                    ),
                    rio.Text(
                        "-" * 40
                    ),
                    spacing=0.2,
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
            rio.Text(
                "[ Refresh ] [ Add Sale ] [ Edit Sale ] [ Delete Sale ]"
            ),
            *rows,
            spacing=0.5,
            margin=2,
        )