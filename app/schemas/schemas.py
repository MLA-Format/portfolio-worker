from pydantic import BaseModel
from datetime import date
from typing import Literal


class SkillOut(BaseModel):
    name: str
    children: list["ChildSkillOut"] | None
    priority: int | None
    icon: str | None
    id: int


class ChildSkillOut(BaseModel):
    name: str
    priority: int | None
    icon: str | None
    id: int


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


class ProjectSkillOut(BaseModel):
    id: int
    name: str
    priority: int | None
    icon: str | None


class ProjectContactOut(BaseModel):
    id: int
    type: Literal["github", "live"]
    name: str
    value: str
    icon: str | None
    link: str | None
    priority: int | None
    show_in_header: bool | None


class ProjectOut(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date | None
    description: str | None
    bulleted_description: list[str]
    image: str | None
    priority: int | None
    skills: list[ProjectSkillOut]
    contacts: list[ProjectContactOut]


class ExperienceOut(BaseModel):
    id: int
    name: str
    title: str
    icon: str | None
    start_date: date
    end_date: date | None
    bulleted_description: list[str]
    priority: int | None


class GeneralOut(BaseModel):
    message: str
