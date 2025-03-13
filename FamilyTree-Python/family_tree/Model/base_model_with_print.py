from pydantic import BaseModel

class BaseModelWithPrint(BaseModel):
    def __str__(self):
        return str(self.model_dump())

    def __repr__(self):
        return self.__str__()