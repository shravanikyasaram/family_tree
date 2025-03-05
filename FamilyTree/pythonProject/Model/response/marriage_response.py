from datetime import date

from Model.base_model_with_print import BaseModelWithPrint
from Model.individuals import Individuals


class MarriageResponse(BaseModelWithPrint):
    wedding_date: date
    husband: Individuals
    wife: Individuals