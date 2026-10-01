# Library imports.
from fastapi import APIRouter

# Custom module imports.
from schemas import SkillOut, ContactOut, EducationOut, GeneralOut

router = APIRouter()

@router.get("/")
async def root() -> GeneralOut:
    return GeneralOut(about_me="API in development.")

@router.get("/skills")
async def get_skills(req: Request) -> list[SkillOut]:
    raise HTTPException(status_code=501, detail="Awaiting implementation.")

@router.get("/contacts")
async def get_contacts(req: Request) -> list[ContactOut]:
    raise HTTPException(status_code=501, detail="Awaiting implementation.")

@router.get("/education")
async def get_education(req: Request) -> list[EducationOut]:
    raise HTTPException(status_code=501, detail="Awaiting implementation.")