from services import accounts, finance, sales, purchases, users, inventory, legal, journal, entry_lines

def main():
    print("=== Accounts ===")
    print(accounts.get_accounts())

    print("=== Finance ===")
    print(finance.get_finance())

    print("=== Sales ===")
    print(sales.get_sales())

    print("=== Purchases ===")
    print(purchases.get_purchases())

    print("=== Users ===")
    print(users.get_users())

    print("=== Inventory ===")
    print(inventory.get_inventory())

    print("=== Legal ===")
    print(legal.get_legal())

    print("=== Journal ===")
    print(journal.get_journal())

    print("=== Entry Lines ===")
    print(entry_lines.get_entry_lines())

if __name__ == "__main__":
    main()
