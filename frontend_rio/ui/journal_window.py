from rio import Window
from services.journal import get_journal

def journal_window(win: Window):
    data = get_journal()
    win.table(data, columns=["id", "date", "operation", "status", "amount"])
