from asyncio import run
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import db_init
from routes.v1 import v1_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db_init()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5050'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(v1_router)

if __name__ == '__main__':
    from uvicorn import Config, Server

    server = Server(config=Config(app='main:app', port=8000, reload=True, use_colors=True))
    run(server.serve())
