# Library imports.
from fastapi import FastAPI, Request
from workers import asgi
import asyncpg

# Custom module imports.
from schemas import SkillOut, ContactOut, EducationOut

app = FastAPI()

# @app.get("/")
# async def root():
#     return {"H12ello": "World"}

# @app.get("/sql_test")
# async def sql_test(req: Request):
#     env = req.scope["env"]
#     try:
#         sql_stmt = await env.PORTFOLIO_DB_BINDING.prepare("SELECT * FROM skills").run()
#         return sql_stmt.get("results", None)
#     except Exception as e:
#         return {"message": "Database query failed",
#                 "error": str(e)}

@app.get("/")
async def root():
    return "API in development."

@app.get("/skills")
async def get_skills(req: Request) -> list[SkillOut]:
    raise HTTPException(status_code=501, detail="Awaiting implementation.")

@app.get("/contacts")
async def get_contacts(req: Request) -> list[ContactOut]:
    raise HTTPException(status_code=501, detail="Awaiting implementation.")

@app.get("/education")
async def get_education(req: Request) -> list[EducationOut]:
    raise HTTPException(status_code=501, detail="Awaiting implementation.")

Default = asgi.entrypoint(app)