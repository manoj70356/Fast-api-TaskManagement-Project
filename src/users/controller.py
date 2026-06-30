from src.users.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from .dtos import UserSchema
from .models import User
from fastapi import HTTPException, status, Request
from pwdlib import PasswordHash
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from src.utils.settings import settings
from datetime import datetime, timedelta



password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register(body: UserSchema, db: Session):

    is_user = db.query(User).filter(User.username == body.username).first()
    if is_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    is_email = db.query(User).filter(User.email == body.email).first()
    if is_email:
        raise HTTPException(
            status_code=400,
            detail="Email address already exists."
        )

    hash_password = get_password_hash(body.password)

    new_user = User(name=body.name, username=body.username, hash_password=hash_password, email=body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "Registration Done"}


def login(body: LoginSchema, db: Session):

    user = db.query(User).filter(User.username == body.username).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    exp_time = datetime.now() + timedelta(seconds=30)

    payload = {
        "_id": user.id,
        "exp": exp_time
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return {
        "token": token,
        "token_type": "bearer"
    }


## token send
def is_authenticated(request: Request, db: Session):
    try:
        auth_header = request.headers.get("authorization")
        if not auth_header:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized..")
        if not auth_header:
            return {"error": "No token provided"}

        token = auth_header.split(" ")[1]  

        data = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        print(data)
        user_id = data.get("_id")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized..")
            

        return user
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized..")