from fastapi import FastAPI, Form, Depends
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from asyncio import run
from database import DataBaseCrud
from database.models import UserModel

from schemas import *
from jwt import JWTBearer, jwt_generator
from exceptions import NotCorrectPassword, UserNotFound

db = DataBaseCrud()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5050'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post('/login', response_model=UserTokenResponse)
async def login(data: UserLoginData = Form()):
    userModel = UserModel(username=data.username, password=data.password)
    try:
        user = await db.get_user(userModel, True)
        if user:
            return UserTokenResponse(
                username=user.username,
                token=jwt_generator.generate_access_token(user.id),
                detail='Success',
            )
    except NotCorrectPassword:
        return UserTokenResponse(username=data.username, detail='Not correct password')
    except UserNotFound:
        return UserTokenResponse(username=data.username, detail='User not found.')


@app.get('/exists', response_model=UserExistsResponse)
async def check_user_exists(username: str):
    userModel = UserModel(username=username)
    if not await db.get_user(userModel):
        return UserExistsResponse(username=username, exists=False)
    return UserExistsResponse(username=username, exists=True)


@app.post('/user', status_code=201, response_model=UserTokenResponse)
async def register(data: UserRegisterData = Form()):
    user = UserModel(
        email=data.email,
        password=data.password,
        username=data.username,
        avatar=await data.avatar.read() if data.avatar else None,
        banner=await data.banner.read() if data.banner else None,
    )
    user_id = await db.add_user(user)
    return UserTokenResponse(
        username=data.username,
        token=jwt_generator.generate_access_token(user_id),
        detail='User created',
    )


@app.get('/user/{username}', response_model=UserResponse)
async def get_user(username: str):
    user_db = await db.get_user(UserModel(username=username))
    if user_db:
        return UserResponse(username=user_db.username, email=user_db.email)
    raise UserNotFound


@app.post('/token', dependencies=[Depends(JWTBearer())])
async def validate_token():
    return {'detail': 'Access granted'}


@app.get('/avatar/{username}')
async def get_user_avatar(username: str):
    user_db = await db.get_user(UserModel(username=username))

    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    if not user_db.avatar:
        raise HTTPException(status_code=404, detail='Avatar not found')

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': f'attachment; filename={username}.png',
    }

    return Response(content=user_db.avatar, media_type='image/png', headers=headers)


if __name__ == '__main__':
    from uvicorn import Config, Server

    run(db.create_tables())

    server = Server(config=Config(app=app, host='127.0.0.1', port=8000, reload=True))
    run(server.serve())
