from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from asyncio import run
from database import DataBaseCrud
from database.models import UserModel

from schemas import *
from jwt import JWTBearer, jwt_generator

db = DataBaseCrud()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5050'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


async def get_user(data: UserLoginData) -> UserModel | None:
    user = UserModel(username=data.username, password=data.password)
    user = await db.get_user(user)
    if user:
        return user
    return None


@app.post('/login')
async def login(data: UserLoginData = Form()):
    user = await get_user(data)
    if user:
        return {'token': jwt_generator.generate_access_token(user.id)}
    raise HTTPException(status_code=404, detail='User not found.')


@app.post('/register', status_code=201)
async def register(data: UserRegisterData = Form()):
    user = UserModel(
        email=data.email,
        password=data.password,
        username=data.username,
        avatar=await data.avatar.read() if data.avatar else None,
        banner=await data.banner.read() if data.banner else None,
    )
    user_id = await db.add_user(user)
    return {'token': jwt_generator.generate_access_token(user_id)}


@app.post('/token', dependencies=[Depends(JWTBearer())])
async def validate_token():
    return {'message': 'Access granted'}


if __name__ == '__main__':
    from uvicorn import Config, Server
    
    run(db.create_tables())

    server = Server(config=Config(app=app, host='127.0.0.1', port=8000, reload=True))
    run(server.serve())
