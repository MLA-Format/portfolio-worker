from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def fetch(self, request):
        return {"Hello": "World"}