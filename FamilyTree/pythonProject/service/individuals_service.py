from fastapi import HTTPException

from repository.individuals_entity import IndividualsEntity
from repository.marriage_entity import MarriageEntity
from service.Logger import get_logger

logger = get_logger(__name__)

def add_first_couple(individuals, db):
    if not individuals.husband or not individuals.wife:
        raise HTTPException(status_code=400, detail='You have to enter both Husband and Wife details.')

    husband = IndividualsEntity(**individuals.husband.model_dump())
    db.add(husband)
    db.flush()
    logger.info("Saving husband details: %s",  husband)

    for wife_data in individuals.wife:
        wife_details = wife_data.model_dump()
        wedding_date = wife_details.pop("wedding_date")
        wife = IndividualsEntity(**wife_details)
        db.add(wife)
        logger.info("Saving wife details: %s", wife)
        db.flush()

        marriage = MarriageEntity(husband_id = husband.id, wife_id = wife.id, wedding_date = wedding_date)
        db.add(marriage)
    db.commit()
