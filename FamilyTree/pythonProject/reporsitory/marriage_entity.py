from sqlalchemy import Column, Integer, Date

from database.database import Base

class MarriageEntity(Base):
    __tablename__ = 'marriage'
    id = Column(Integer, primary_key=True, index=True)
    husband_id = Column(Integer, nullable=False)
    wife_id = Column(Integer, nullable=False)
    wedding_date = Column(Date, nullable=True)

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if not k.startswith("_")})

    def __repr__(self):
        return self.__str__()
