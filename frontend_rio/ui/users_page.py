# frontend_rio/ui/users_page.py
from rio import PageView, Table, AutoForm, TextInput
from services.users import get_users, add_user_entry

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
    page.add(Table(data, columns=["id", "username", "role", "email"]))

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Ім'я користувача", name="username"))
    form.add(TextInput(label="Роль (admin/manager/employee)", name="role"))
    form.add(TextInput(label="Email", name="email"))

    def on_submit(values):
        ok, msg = validate_user_entry(values["username"], values["role"], values["email"])
        if not ok:
            page.alert(msg)  # показати помилку
        else:
            add_user_entry(values)  # виклик сервісу
            page.toast("Користувача успішно додано")

    form.on_submit(on_submit)
    page.add(form)

    return page
