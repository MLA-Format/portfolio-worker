# Library imports.
from fastapi import APIRouter, Request

# Custom module imports.
from schemas import SkillOut, ContactOut, EducationOut, GeneralOut
from internal import db_get_skills, db_get_contacts

router = APIRouter()

@router.get("/")
async def root() -> GeneralOut:
    return GeneralOut(about_me="API in development.")

@router.get("/skills")
async def get_skills(req: Request) -> list[SkillOut]:
    return await db_get_skills(req.scope["env"])

@router.get("/contacts")
async def get_contacts(req: Request) -> list[ContactOut]:
    return await db_get_contacts(req.scope["env"])

@router.get("/education")
async def get_education(req: Request) -> list[EducationOut]:
    raise HTTPException(status_code=501, detail="Awaiting implementation.")