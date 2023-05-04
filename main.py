from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from v1.router import router


app = FastAPI(
    title='Ensaware'
)

app.include_router(router)