import rio

from services.legal import get_legal


@rio.page(
    name="Legal",
    url_segment="legal"
)
class LegalPage(rio.Component):

    def build(self) -> rio.Component:

        entries = get_legal()

        rows = [
            rio.Text(
                "ID | Contract | Partner | Status",
                style="heading3"
            ),
            rio.Text(
                "[ Refresh ] [ Add Contract ] [ Edit Contract ] [ Delete Contract ]"
            ),
            rio.Text(
                "-" * 80
            ),
        ]

        for entry in entries:
            rows.append(
                rio.Text(
                    f"{entry['id']} | "
                    f"{entry['contract']} | "
                    f"{entry['partner']} | "
                    f"{entry['status']}"
                )
            )

        return rio.Column(
            rio.Text(
                "Legal",
                style="heading2"
            ),
            rio.Text(
                f"Records: {len(entries)}"
            ),
            rio.Text(
                "Legal API Connected",
                style="heading3"
            ),
            *rows,
            spacing=0.5,
            margin=2,
        )