from typing import List

from Model.base_model_with_print import BaseModelWithPrint

from Model.wife import Wife


class Spouse(BaseModelWithPrint):
    individual_id: int
    partner: List[Wife]