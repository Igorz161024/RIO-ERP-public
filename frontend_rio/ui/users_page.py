from rio import PageView, Table, AutoForm, TextInput
from services.users import get_users, add_user_entry, delete_user_entry
from ui.messages import show_error, show_info, show_success, show_warning

# 🔹 Допустимі ролі користувачів
ALLOWED_ROLES = ["admin", "manager", "employee"]

# 🔹 Допоміжна функція для перевірки введених даних
def validate_user_entry(username, role, email):
    if not username.strip():
        return False, "Ім'я користувача не може бути порожнім"
    if role not in ALLOWED_ROLES:
        return False, f"Недопустима роль. Дозволені: {', '.join(ALLOWED_ROLES)}"
    if "@" not in email or "." not in email:
        return False, "Невірний формат email"
    return True, "OK"

# 🔹 Основна функція сторінки
def users_page(page: PageView):
    # показ таблиці з бекенду
    data = get_users()
    if not data:
        show_info(page, "Немає користувачів у системі")
    else:
        table = Table(
            data,
            columns=["id", "username", "role", "email"],
            actions=[{"label": "Видалити", "name": "delete_user"}]
        )

        # обробка дій у таблиці
        def on_action(action, row):
            if action == "delete_user":
                # попередження перед видаленням
                show_warning(page, f"Ви дійсно хочете видалити користувача {row['username']}?")
                try:
                    delete_user_entry(row["id"])
                    show_success(page, "Користувача успішно видалено")
                except Exception as e:
                    show_error(page, f"Помилка при видаленні: {str(e)}")

        table.on_action(on_action)
        page.add(table)

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Ім'я користувача", name="username"))
    form.add(TextInput(label="Роль (admin/manager/employee)", name="role"))
    form.add(TextInput(label="Email", name="email", placeholder="user@example.com"))

    def on_submit(values):
        ok, msg = validate_user_entry(values["username"], values["role"], values["email"])
        if not ok:
            show_error(page, msg)
        else:
            try:
                add_user_entry(values)
                show_success(page, "Користувача успішно додано")
                form.clear()  # очистити форму після успішного додавання
            except Exception as e:
                show_error(page, f"Помилка при додаванні: {str(e)}")

    form.on_submit(on_submit)
    page.add(form)

    return page
