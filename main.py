from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import contacts, users, auth
import redis.asyncio as redis
from src.conf.config import settings  # для обмеження кількості запитів

from fastapi_limiter import FastAPILimiter


app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.on_event("startup")  # для обмеження кількості запитів
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app,
    such as connecting to databases or initializing caches.

    :return: A future
    :doc-author: Trelent
    """

    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    await FastAPILimiter.init(r)


# Додаємо CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # список джерел, яким дозволено доступ до застосунку
    allow_credentials=True,  # True означає, що дозволені кросдоменні запити з урахуванням облікових даних
    allow_methods=["*"],  # список дозволених методів HTTP
    allow_headers=["*"],  # список дозволених заголовків HTTP
)


@app.get("/")
def read_root():
    """
    The read_root function

    :return: dct
    """

    return {"message": "Hello World"}
