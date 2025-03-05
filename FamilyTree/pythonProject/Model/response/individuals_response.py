from datetime import date
from typing import Optional

from Model.base_model_with_print import BaseModelWithPrint


class IndividualsResponse(BaseModelWithPrint):
    first_name: str
    last_name: str
    date_of_birth: date
    date_of_death: Optional[date] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    occupation: Optional[str] = None
    relation_type: Optional[str] = None