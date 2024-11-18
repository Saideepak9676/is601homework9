from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# OAuth2PasswordBearer is used for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fake users data for testing
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "secret",
        "full_name": "Admin User",
        "email": "admin@example.com",
    }
}

class User(BaseModel):
    username: str
    password: str

class QRCodeRequest(BaseModel):
    url: str
    fill_color: str
    back_color: str
    size: int

@app.post("/token")
async def login_for_access_token(form_data: User):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": "fake-access-token", "token_type": "bearer"}

@app.post("/qr-codes/")
async def create_qr_code(qr_request: QRCodeRequest, token: str = Depends(oauth2_scheme)):
    if token != "fake-access-token":  # Fake token check for testing
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "QR code created successfully", "data": qr_request}