# Library imports.
from fastapi import FastAPI, Request
from workers import asgi
import logging

# Module imports.
from routers import router

# Creating logger.
logger = logging.getLogger(__name__)

# Create api
app = FastAPI()
app.include_router(router)

Default = asgi.entrypoint(app)
