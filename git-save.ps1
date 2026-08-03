param(
    [string]$Message = "Update project"
)

git add .
git commit -m $Message
git pull origin main --allow-unrelated-histories --no-edit
git pull public main --allow-unrelated-histories --no-edit
git push origin main
git push public main
