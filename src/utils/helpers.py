from fastapi import Request, HTTPException, status, Depends
from src.utils.settings import settings
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from src.users.models import User
from src.utils.db import get_db



## token send
def is_authenticated(request: Request, db: Session = Depends(get_db)):
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