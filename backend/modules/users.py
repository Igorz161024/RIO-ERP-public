from backend.modules.db import insert_user, update_user, delete_user
class User:
    def __init__(self, username, role):
        # Ініціалізація атрибутів класу
        self.username = username
        self.role = role

        # Автоматично додаємо користувача в базу при створенні
        insert_user(self.username, self.role)

    def __str__(self):
        # Метод для красивого виводу об’єкта
        return f"User(username={self.username}, role={self.role})"

    def update(self, user_id, username=None, role=None):
        # Виклик функції з db.py для оновлення запису
        update_user(user_id, username, role)

    def delete(self, user_id):
        # Виклик функції з db.py для видалення запису
        delete_user(user_id)