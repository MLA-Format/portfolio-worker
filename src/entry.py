from fastapi import FastAPI, Request
from workers import asgi
import asyncpg

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

@app.get("/sql_test")
async def sql_test(req: Request):
    env = req.scope["env"]

    try:
        hyperdrive = env.HYPERDRIVE

        db_conn = await asyncpg.connect(
            host=hyperdrive.host,
            port=int(hyperdrive.port),
            user=hyperdrive.user,
            password=hyperdrive.password,
            database=hyperdrive.database,
            ssl=False,
        )

        db_res = await db_conn.fetch("SELECT * FROM skills")

        return [dict(row) for row in db_res]
    finally:
        await db_conn.close()

Default = asgi.entrypoint(app)