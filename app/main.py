from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import create_table, delete_tables
from app.routers import (gen_recommendation_router, item_router,
                         purchase_router, recommendation_router, user_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    print('start')
    yield
    # await delete_tables()
    print('end')

app = FastAPI(lifespan=lifespan)


app.include_router(user_router)
app.include_router(item_router)
app.include_router(purchase_router)
app.include_router(recommendation_router)
app.include_router(gen_recommendation_router)
