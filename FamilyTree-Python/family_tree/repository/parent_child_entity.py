from sqlalchemy import Column, Integer, ForeignKey

from database.database import Base

class ParentChildEntity(Base):
    __tablename__ = "parent_child"
    child_id = Column(Integer, ForeignKey("individuals.id", ondelete="CASCADE"), primary_key=True)
    father_id = Column(Integer, ForeignKey("individuals.id", ondelete="CASCADE"), primary_key=True)
    mother_id = Column(Integer, ForeignKey("individuals.id", ondelete="CASCADE"), primary_key=True)

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if not k.startswith("_")})

    def __repr__(self):
        return self.__str__()
