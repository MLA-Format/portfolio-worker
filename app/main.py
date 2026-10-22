# Library imports.
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from workers import asgi
import logging

# Module imports.
from routers import router

# Creating logger.
logger = logging.getLogger(__name__)

# Create api
app = FastAPI()

# Allow cross-origin requests from the frontend.
# TODO: Replace "*" with the website's domain before going live.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
)

app.include_router(router)

Default = asgi.entrypoint(app)
