# frontend_rio/ui/legal_page.py
from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.legal import get_legal, add_legal_entry
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
    page.add(Table(data, columns=["id", "date", "case_number", "description", "amount"]))

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date"))
    form.add(TextInput(label="Номер справи", name="case_number"))
    form.add(TextInput(label="Опис", name="description"))
    form.add(NumberInput(label="Сума", name="amount"))

    def on_submit(values):
        ok, msg = validate_legal_entry(values["date"], values["case_number"], values["description"], values["amount"])
        if not ok:
            page.alert(msg)  # показати помилку
        else:
            add_legal_entry(values)  # виклик сервісу
            page.toast("Юридичний запис успішно додано")

    form.on_submit(on_submit)
    page.add(form)

    return page
