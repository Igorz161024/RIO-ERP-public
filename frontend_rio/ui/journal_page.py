from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.journal import get_journal, add_journal_entry, delete_journal_entry
from ui.messages import show_error, show_info, show_success, show_warning
import datetime

# 🔹 Допоміжна функція для перевірки введених даних
def validate_journal_entry(date, operation, amount, status):
    if not date.strip():
        return False, "Дата не може бути порожньою"
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False, "Невірний формат дати (YYYY-MM-DD)"

    if not operation.strip():
        return False, "Операція не може бути порожньою"

    if not isinstance(amount, (int, float)) or amount <= 0:
        return False, "Сума має бути числом > 0"

    if not status.strip():
        return False, "Статус не може бути порожнім"

    return True, "OK"

# 🔹 Основна функція сторінки
def journal_page(page: PageView):
    # показ таблиці з бекенду
    data = get_journal()
    if not data:
        show_info(page, "Немає записів у журналі")
    else:
        table = Table(
            data,
            columns=["id", "date", "operation", "status", "amount"],
            actions=[{"label": "Видалити", "name": "delete_journal"}]
        )

        # обробка дій у таблиці
        def on_action(action, row):
            if action == "delete_journal":
                show_warning(page, f"Ви дійсно хочете видалити запис {row['id']}?")
                try:
                    delete_journal_entry(row["id"])
                    show_success(page, "Запис у журналі успішно видалено")
                except Exception as e:
                    show_error(page, f"Помилка при видаленні: {str(e)}")

        table.on_action(on_action)
        page.add(table)

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date", placeholder="2026-10-11"))
    form.add(TextInput(label="Операція", name="operation"))
    form.add(NumberInput(label="Сума", name="amount", placeholder="1000"))
    form.add(TextInput(label="Статус", name="status"))

    def on_submit(values):
        ok, msg = validate_journal_entry(values["date"], values["operation"], values["amount"], values["status"])
        if not ok:
            show_error(page, msg)
        else:
            try:
                add_journal_entry(values)
                show_success(page, "Запис у журнал успішно додано")
                form.clear()  # очистити форму після успішного додавання
            except Exception as e:
                show_error(page, f"Помилка при додаванні: {str(e)}")

    form.on_submit(on_submit)
    page.add(form)

    return page
