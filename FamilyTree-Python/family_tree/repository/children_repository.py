from sqlalchemy import or_

from repository.individuals_entity import IndividualsEntity
from repository.parent_child_entity import ParentChildEntity


def get_children(parent_id, db):
    return (db.query(IndividualsEntity)
            .join(ParentChildEntity, ParentChildEntity.child_id == IndividualsEntity.id)
            .filter(or_(ParentChildEntity.father_id == parent_id, ParentChildEntity.mother_id == parent_id))
            .all())
