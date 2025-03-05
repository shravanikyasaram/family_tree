from fastapi import HTTPException

from Model.individuals import Individuals
from Model.response.marriage_response import MarriageResponse
from repository.individuals_entity import IndividualsEntity
from repository.individuals_repository import find_by_individuals_id
from repository.marriage_entity import MarriageEntity
from repository.spouse_repository import get_spouse, get_couple
from service.Logger import get_logger
from util.family_tree_util import check_if_user_already_exist

logger = get_logger(__name__)

def add_new_spouse(spouse_details, db):
    individual_id = spouse_details.individual_id
    individual_id_from_db = find_by_individuals_id(individual_id, db)

    if not spouse_details or not spouse_details.individual_id or individual_id_from_db is None:
        raise HTTPException(status_code=400, detail='Invalid Spouse details')

    check_if_user_already_exist(spouse_details, db)

    for partner in spouse_details.partner:
        spouse = partner.model_dump()
        wedding_date = spouse.pop("wedding_date")
        spouse_entity = IndividualsEntity(**spouse)
        db.add(spouse_entity)
        db.flush()
        logger.info("Spouse details: %s", spouse_entity)

        marriage = MarriageEntity(husband_id=individual_id, wife_id=spouse_entity.id, wedding_date=wedding_date)
        db.add(marriage)
    db.commit()

def get_spouse_details(spouse_id, db):
    spouse_data = get_spouse(spouse_id, db)

    if not spouse_data:
        raise HTTPException(status_code=200, detail='No details found')

    logger.info("Getting spouse details for: %s", {spouse_id})
    spouse_list = []
    for spouse, marriage in spouse_data:
        spouse_dict = {k: v for k, v in spouse.__dict__.items()}
        spouse_list.append({
            "spouse": spouse_dict,
            "wedding_date": marriage.wedding_date
        })
    return spouse_list

def get_couple_details(individual_id, db):
    marriage, husband_details, wife_details =  get_couple(individual_id, db)

    if not marriage or not husband_details or not wife_details:
        raise HTTPException(status_code=500, detail='No marriage details found')

    return MarriageResponse(
        wedding_date = marriage.wedding_date,
        husband = Individuals(**husband_details.__dict__),
        wife = Individuals(**wife_details.__dict__)
    )
