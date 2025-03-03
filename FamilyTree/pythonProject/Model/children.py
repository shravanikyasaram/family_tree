from typing import List

from Model.individuals import Individuals

from pydantic import BaseModel

class Children(BaseModel):
    children: List[Individuals]
    father_id: int
    mother_id: int
