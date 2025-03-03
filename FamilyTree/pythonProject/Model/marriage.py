from datetime import date

from pydantic import BaseModel

class Marriage(BaseModel):
    husband_id: int
    wife_id: int
    wedding_date: date
