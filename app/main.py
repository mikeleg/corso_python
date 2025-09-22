from fastapi import FastAPI

from app.api.characters import router as characters_router
from app.api.planets import router as planets_router
from app.api.starships import router as starships_router
from app.db import create_db_and_tables, populate_sample_data

app = FastAPI(title="Star Wars API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    populate_sample_data()


app.include_router(characters_router)
app.include_router(planets_router)
app.include_router(starships_router)
