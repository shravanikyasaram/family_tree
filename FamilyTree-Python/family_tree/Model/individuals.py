from datetime import date
from typing import Optional

from Model.base_model_with_print import BaseModelWithPrint

class Individuals(BaseModelWithPrint):
    first_name: str
    last_name: str
    nick_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    occupation: Optional[str] = None
