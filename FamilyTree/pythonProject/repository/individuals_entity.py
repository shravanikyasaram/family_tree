from sqlalchemy import Column, Integer, String, Date
from database.database import Base

class IndividualsEntity(Base):
    __tablename__ = 'individuals'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), index=True, nullable=False)
    last_name = Column(String(100), index=True, nullable=False)
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    date_of_death = Column(Date, nullable=True)
    location = Column(String(100), nullable=True)
    occupation = Column(String(100), nullable=True)

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if not k.startswith("_")})

    def __repr__(self):
        return self.__str__()
