from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Конфігурація JWT
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------------------
# Генерація токена
# -------------------------------
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # тут можна зробити перевірку користувача з БД
    if form_data.username != "admin" or form_data.password != "1234":
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": form_data.username, "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# -------------------------------
# Перевірка токена
# -------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# -------------------------------
# CRUD приклад для accounts
# -------------------------------
fake_db = []

@app.get("/api/accounts/")
def get_accounts(current_user: str = Depends(get_current_user)):
    return fake_db

@app.post("/api/accounts/")
def create_account(account: dict, current_user: str = Depends(get_current_user)):
    account["id"] = len(fake_db) + 1
    fake_db.append(account)
    return account

@app.put("/api/accounts/{account_id}")
def update_account(account_id: int, account: dict, current_user: str = Depends(get_current_user)):
    for acc in fake_db:
        if acc["id"] == account_id:
            acc.update(account)
            return acc
    raise HTTPException(status_code=404, detail="Account not found")

@app.delete("/api/accounts/{account_id}")
def delete_account(account_id: int, current_user: str = Depends(get_current_user)):
    for acc in fake_db:
        if acc["id"] == account_id:
            fake_db.remove(acc)
            return {"detail": "Account deleted"}
    raise HTTPException(status_code=404, detail="Account not found")

# -------------------------------
# Підключення нового роутера users
# -------------------------------
from backend.routers import users_router
app.include_router(users_router.router)
