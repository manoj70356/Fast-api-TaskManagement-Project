from fastapi import APIRouter
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.users.dtos import UserSchema, UserResponseSchema,LoginSchema, TokenResponse
from src.users import controller
from fastapi import status, HTTPException, Request
from src.users.controller import register, login
from fastapi import FastAPI, Depends


user_routes = APIRouter(prefix="/user")


@user_routes.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session=Depends(get_db)):
    return controller.register(body, db)


@user_routes.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(body:LoginSchema, db: Session=Depends(get_db)):
    return controller.login(body, db)




@user_routes.get("/is_auth", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def is_auth(request:Request,  db: Session=Depends(get_db)):
    return controller.is_authenticated(request, db)