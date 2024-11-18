from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://assignment-fastapi-1.onrender.com/"],  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be sent
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run("app.auth:app", host="0.0.0.0", port=port, reload=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        return {"message": "Username already registered"}
    
    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        return {"message": "Email already registered"}

    hashed_password = utils.hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User registered successfully"}

@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid user name")
    
    if not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token = utils.create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    db_users = db.query(models.User).all()
    if not db_users:
        raise HTTPException(status_code=404, detail="No users found")
    return db_users  

@app.post("/recover-password")
def recover_password(credentials: schemas.PasswordRecovery, db: Session = Depends(get_db)):

    db_user = (db.query(models.User).filter((models.User.username == credentials.username_or_email) |(models.User.email == credentials.username_or_email)).first())

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not utils.verify_password(credentials.old_password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    new_hashed_password = utils.hash_password(credentials.new_password)

    db_user.hashed_password = new_hashed_password
    db.commit()
    db.refresh(db_user)

    return {"message": "Password updated successfully"}


