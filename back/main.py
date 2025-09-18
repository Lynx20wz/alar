from fastapi import FastAPI, Form, UploadFile
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
async def login(data: UserBaseData):
    return {'exists': await check_user_exist(data)}


@app.post('/register')
async def register(
    email: str = Form(...),
    password: str = Form(...),
    username: str = Form(...),
    avatar: Optional[UploadFile] = Form(None),
    banner: Optional[UploadFile] = Form(None),
):
    user = UserModel(
        email=email,
        password=password,
        username=username,
        avatar=await avatar.read() if avatar else None,
        banner=await banner.read() if banner else None,
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
