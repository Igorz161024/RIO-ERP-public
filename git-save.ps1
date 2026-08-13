param(
    [string]$Message = "Update project"
)

# Встановлюємо правильне кодування для консолі
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 > $null

# Додаємо всі зміни
git add .

# Коміт з повідомленням
git commit -m $Message

# Пул з приватного та публічного репозиторіїв
git pull origin main --allow-unrelated-histories --no-edit
git pull public main --allow-unrelated-histories --no-edit

# Пуш у приватний та публічний репозиторії
git push origin main
git push public main

Write-Output "✅ Зміни збережено і відправлено у приватний та публічний репозиторії."
