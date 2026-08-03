import rio
from rio import App, Window
import httpx
from config import API_URL

app = App()

@app.window(title="RIO ERP", size=(1200, 800))
def main(win: Window):
    response = httpx.get(f"{API_URL}/api/journal")
    data = response.json()
    win.table(data, columns=["id", "date", "operation", "status", "amount"])

if __name__ == "__main__":
    app.run()
