from asyncio import run
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import create_tables
from exceptions import setup_exception_handlers
from routes import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5050'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

for router in all_routers:
    app.include_router(router)

setup_exception_handlers(app)

if __name__ == '__main__':
    from uvicorn import Config, Server

    server = Server(config=Config(app='main:app', port=8000, reload=True, use_colors=True))
    run(server.serve())
