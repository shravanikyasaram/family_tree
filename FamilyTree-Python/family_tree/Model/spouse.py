from typing import List

from Model.base_model_with_print import BaseModelWithPrint

from Model.partner import Partner


class Spouse(BaseModelWithPrint):
    individual_id: int
    partner: List[Partner]