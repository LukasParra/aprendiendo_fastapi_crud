from fastapi import FastAPI
from Routes import crud

app = FastAPI()
app.include_router(crud.router)

