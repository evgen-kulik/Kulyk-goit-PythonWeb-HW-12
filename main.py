from fastapi import FastAPI
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
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
