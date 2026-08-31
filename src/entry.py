from fastapi import FastAPI
from workers import asgi

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "World"}

Default = asgi.entrypoint(app)