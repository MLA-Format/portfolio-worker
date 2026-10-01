from pydantic import BaseModel
from datetime import date

class SkillOut(BaseModel):
    name: str
    children: list["Skill"] | None
    priority: int | None
    icon: str | None

class ContactOut(BaseModel):
    name: str
    value: str
    icon: str | None
    link: str | None
    priority: int | None
    show_in_header: bool | None

class EducationOut(BaseModel):
    school: str
    degree: str
    start_date: date
    end_date: date | None
    image: str | None