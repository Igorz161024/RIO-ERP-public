from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.legal import get_legal, add_legal_entry, delete_legal_entry
from ui.messages import show_error, show_info, show_success, show_warning
import datetime

# 🔹 Допоміжна функція для перевірки введених даних
def validate_legal_entry(date, case_number, description, amount):
    if not date.strip():
        return False, "Дата не може бути порожньою"
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False, "Невірний формат дати (YYYY-MM-DD)"

    if not case_number.strip():
        return False, "Номер справи не може бути порожнім"

    if not description.strip():
        return False, "Опис не може бути порожнім"

    if not isinstance(amount, (int, float)) or amount <= 0:
        return False, "Сума має бути числом > 0"

    return True, "OK"

# 🔹 Основна функція сторінки
def legal_page(page: PageView):
    # показ таблиці з бекенду
    data = get_legal()
    if not data:
        show_info(page, "Немає юридичних записів")
    else:
        table = Table(
            data,
            columns=["id", "date", "case_number", "description", "amount"],
            actions=[{"label": "Видалити", "name": "delete_legal"}]
        )

        # обробка дій у таблиці
        def on_action(action, row):
            if action == "delete_legal":
                show_warning(page, f"Ви дійсно хочете видалити справу №{row['case_number']}?")
                try:
                    delete_legal_entry(row["id"])
                    show_success(page, "Юридичний запис успішно видалено")
                except Exception as e:
                    show_error(page, f"Помилка при видаленні: {str(e)}")

        table.on_action(on_action)
        page.add(table)

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date", placeholder="2026-10-11"))
    form.add(TextInput(label="Номер справи", name="case_number"))
    form.add(TextInput(label="Опис", name="description"))
    form.add(NumberInput(label="Сума", name="amount", placeholder="1000"))

    def on_submit(values):
        ok, msg = validate_legal_entry(values["date"], values["case_number"], values["description"], values["amount"])
        if not ok:
            show_error(page, msg)
        else:
            try:
                add_legal_entry(values)
                show_success(page, "Юридичний запис успішно додано")
                form.clear()  # очистити форму після успішного додавання
            except Exception as e:
                show_error(page, f"Помилка при додаванні: {str(e)}")

    form.on_submit(on_submit)
    page.add(form)

    return page
