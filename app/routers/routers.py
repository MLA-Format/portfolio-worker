# Library imports.
from fastapi import APIRouter, Request

# Custom module imports.
from schemas import SkillOut, ContactOut, EducationOut, GeneralOut
from internal import db_get_skills

router = APIRouter()

@router.get("/")
async def root() -> GeneralOut:
    return GeneralOut(about_me="API in development.")

# -> list[SkillOut]
@router.get("/skills")
async def get_skills(req: Request):
    return await db_get_skills(req.scope["env"])

@router.get("/contacts")
async def get_contacts(req: Request) -> list[ContactOut]:
    raise HTTPException(status_code=501, detail="Awaiting implementation.")

@router.get("/education")
async def get_education(req: Request) -> list[EducationOut]:
    raise HTTPException(status_code=501, detail="Awaiting implementation.")