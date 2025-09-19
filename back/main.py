from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from asyncio import run
from database import DataBaseCrud
from database.models import UserModel

from schemas import *

db = DataBaseCrud()
app = FastAPI()


async def check_user_exist(data: UserBaseData):
    user = UserModel(email=data.email, password=data.password)
    user = await db.get_user(user)
    if user:
        return True
    return False


@app.post('/login')
async def login(data: UserBaseData = Form()):
    return {'exists': await check_user_exist(data)}


@app.post('/register')
async def register(data: UserRegisterData = Form()):
    user = UserModel(
        email=data.email,
        password=data.password,
        username=data.username,
        avatar=data.avatar.read() if data.avatar else None,
        banner=data.banner.read() if data.banner else None,
    )
    await db.add_user(user)
    return {'status': 'ok'}


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    from uvicorn import Config, Server

    server = Server(config=Config(app=app, host='127.0.0.1', port=8000, reload=True))
    run(server.serve())
