from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from asyncio import run
from database import DataBaseCrud

from exceptions import setup_exception_handlers
from apis import *

db = DataBaseCrud()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_tables()
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

    server = Server(config=Config(app='main:app', host='127.0.0.1', port=8000, reload=True))
    run(server.serve())
