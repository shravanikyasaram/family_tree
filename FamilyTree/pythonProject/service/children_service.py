from fastapi import HTTPException

from repository.children_repository import get_children
from repository.individuals_entity import IndividualsEntity
from repository.parent_child_entity import ParentChildEntity
from service.Logger import get_logger

logger = get_logger(__name__)

def add_children(individuals, db):
    if not individuals.father_id or not individuals.mother_id:
        raise HTTPException(status_code=400, detail='Invalid Children details.')

    children_entities = []
    for child in individuals.children:
        child_details = child.model_dump()
        child_entity = IndividualsEntity(**child_details)
        db.add(child_entity)
        logger.info('child details %s', child_entity)
        children_entities.append(child_entity)

    db.flush()

    for children in children_entities:
        parents_child_entity = ParentChildEntity(child_id = children.id, father_id = individuals.father_id,
                                       mother_id = individuals.mother_id)

        logger.info('parent ids saved %s', parents_child_entity)
        db.add(parents_child_entity)

    db.commit()

def get_children_details(parent_id, db):
    return sorted(get_children(parent_id, db), key=lambda x: x.date_of_birth)
