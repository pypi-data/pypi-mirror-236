from fastapi import FastAPI
from axdocsystem.src.db import setup_db, get_uowf
from axdocsystem.src.settings import Settings


app = FastAPI()
settings = Settings()  # type: ignore
uowf = get_uowf(settings)


@app.on_event("startup")
async def startup():
    await setup_db(uowf)

