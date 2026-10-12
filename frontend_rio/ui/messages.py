def show_error(page, msg: str):
    page.alert(f"❌ Помилка: {msg}", type="error")

def show_info(page, msg: str):
    page.alert(f"ℹ️ {msg}", type="info")

def show_success(page, msg: str):
    page.toast(f"✅ {msg}", duration=3000)

def show_warning(page, msg: str):
    page.alert(f"⚠️ Увага: {msg}", type="warning")
