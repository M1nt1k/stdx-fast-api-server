import os
from fastapi import APIRouter, Body, HTTPException, status
from typing import Optional, List
from app.internal.schemas.models import Token, TokenData, User, PyObjectId, UserModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.pkg.mongo_tools.tools import MongoTools
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger

router = APIRouter(
    prefix=f'/api/v{os.getenv("VERSION")}/users',
    tags=['Users']
)


collection = 'users'

jwt_settings = {
    'Alg': 'HS256',
    'Expire': 30
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@router.get('/{vk_id}', response_model=UserModel)
async def get_user(vk_id: str):
    if (user :=  await MongoTools.find_one(collection=collection, filter={"_id": vk_id})) is not None:
        return user
    
    raise HTTPException(status_code=404, detail=f"User {vk_id} not found")

@router.post('/create', response_model=UserModel)
async def create_user(vk_id: str):
    document = jsonable_encoder(User(vk=vk_id, hashed_password=get_password_hash(vk_id)))
    new_user = await MongoTools.insert_one(collenction=collection, document=document)
    created_user = await MongoTools.find_one(collection=collection, filter={"_id": new_user.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

@router.post('/token')
def get_user_token():
    ...

@router.post('/token/verify')
def verify_token(token: str):
    ...

@router.post('/token/refresh')
def refresh_token(token: str):
    ...
