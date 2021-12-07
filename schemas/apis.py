from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class ApiBase(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = "Remote"
    description: Optional[str] = None
    date_posted: Optional[date] = datetime.now().date()


class ApiCreate(ApiBase):
    name: str
    provider: str
    category: str
    description: str


class ShowApi(ApiBase):
    name: str
    provider: str
    url: Optional[str]
    category: str
    date_posted: date
    description: Optional[str]

    class Config():
        orm_mode = True


