from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asyncio import run
from pydantic import BaseModel
from database import DataBaseCrud
from database.models import UserModel

db = DataBaseCrud()
app = FastAPI()


class UserBaseData(BaseModel):
    email: str
    password: str


@app.post('/login')
async def login(data: UserBaseData):
    return {'status': 'ok'}


@app.post('/register')
async def register(data: UserBaseData):
    return {'status': 'ok'}


@app.post('/baseRegister')
async def baseRegister(data: UserBaseData):
    return {'exist': True} #TODO FOR TESTS!!!
    user = UserModel(email=data.email, password=data.password)
    user = await db.get_user(user)
    if user:
        return {'exist': True}
    # return {'exist': False}


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


async def start_fastapi():
    from uvicorn import Config, Server

    await db.create_tables()

    server = Server(config=Config(app=app, host='127.0.0.1', port=8000, reload=True))
    await server.serve()


if __name__ == '__main__':
    try:
        run(start_fastapi())
    except KeyboardInterrupt:
        pass
