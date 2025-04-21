from typing import List

from Model.base_model_with_print import BaseModelWithPrint
from Model.individuals import Individuals
from Model.partner import Partner

class FirstCouple(BaseModelWithPrint):
    husband: Individuals
    wife: List[Partner]