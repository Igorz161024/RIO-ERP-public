import rio

from services.inventory import get_inventory


@rio.page(
    name="Inventory",
    url_segment="inventory"
)
class InventoryPage(rio.Component):

    def build(self) -> rio.Component:

        items = get_inventory()

        rows = [
            rio.Text(
                "ID | Product | Quantity | Batch | Price",
                style="heading3"
            ),
            rio.Text(
                "[ Refresh ] [ Add Product ] [ Edit Product ] [ Delete Product ]"
            ),
            rio.Text(
                "-" * 70
            ),
        ]

        for item in items:

            rows.append(
                rio.Text(
                    f"{item['id']} | "
                    f"{item['product']} | "
                    f"{item['quantity']} | "
                    f"{item['batch']} | "
                    f"{item['price']}"
                )
            )

        return rio.Column(
            rio.Text(
                "Inventory",
                style="heading2"
            ),
            rio.Text(
                f"Records: {len(items)}"
            ),
            rio.Text(
                "Inventory API Connected",
                style="heading3"
            ),
            *rows,
            spacing=0.5,
            margin=2,
        )