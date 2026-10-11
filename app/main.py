# Library imports.
from fastapi import FastAPI, Request
from workers import asgi
import logging

# Module imports.
from routers import router

# Creating logger.
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)

Default = asgi.entrypoint(app)

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