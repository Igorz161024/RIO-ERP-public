import rio

from services.users import get_users


@rio.page(
    name="Users",
    url_segment="users"
)
class UsersPage(rio.Component):

    def build(self) -> rio.Component:

        entries = get_users()

        rows = [
            rio.Text(
                "ID | Username | Email | Role",
                style="heading3"
            ),
            rio.Text(
                "[ Refresh ] [ Add User ] [ Edit User ] [ Delete User ]"
            ),
            rio.Text(
                "-" * 80
            ),
        ]

        for entry in entries:
            rows.append(
                rio.Text(
                    f"{entry['id']} | "
                    f"{entry['username']} | "
                    f"{entry['email']} | "
                    f"{entry['role']}"
                )
            )

        return rio.Column(
            rio.Text(
                "Users",
                style="heading2"
            ),
            rio.Text(
                f"Records: {len(entries)}"
            ),
            rio.Text(
                "Users API Connected",
                style="heading3"
            ),
            *rows,
            spacing=0.5,
            margin=2,
        )