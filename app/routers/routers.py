# Library imports.
from fastapi import APIRouter, Request

# Custom module imports.
from schemas import SkillOut, ContactOut, EducationOut, GeneralOut, ProjectOut
from internal import db_get_skills, db_get_contacts, db_get_education, db_get_projects

router = APIRouter()

@router.get("/")
async def root() -> GeneralOut:
    return GeneralOut(about_me="API in development.")

@router.get("/skills")
async def get_skills(req: Request):
    return await db_get_skills(req.scope["env"])

@router.get("/contacts")
async def get_contacts(req: Request) -> list[ContactOut]:
    return await db_get_contacts(req.scope["env"])

@router.get("/education")
async def get_education(req: Request) -> list[EducationOut]:
    return await db_get_education(req.scope["env"])


@router.get("/projects")
async def get_projects(req: Request) -> list[ProjectOut]:
    return await db_get_projects(req.scope["env"])
