from fastapi import HTTPException

from Model.response.individuals_response import IndividualsResponse
from repository.individuals_entity import IndividualsEntity
from repository.individuals_repository import get_family_tree, get_individual_id_by_last_name
from repository.marriage_entity import MarriageEntity
from service.Logger import get_logger
from util.family_tree_util import check_if_user_already_exist

logger = get_logger(__name__)

def add_first_couple(individuals, db):
    if not individuals.husband or not individuals.wife:
        raise HTTPException(status_code=400, detail='You have to enter both Husband and Wife details.')

    check_if_user_already_exist(individuals, db)

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

def get_family_tree_details(last_name, db):
    individual_id = get_individual_id_by_last_name(last_name, db)
    if not individual_id:
        raise HTTPException(status_code=500, detail='Last Name not found')

    logger.info("individual_id is: %s", individual_id)
    family_details = get_family_tree(individual_id, db)
    individuals_list = []

    for individual_details in family_details:
        logger.info("each individual_details are: %s", individual_details)
        individual = IndividualsResponse(**{
            "first_name": individual_details[1],
            "last_name": individual_details[2],
            "nick_name": individual_details[3],
            "gender": individual_details[4],
            "date_of_birth": individual_details[5],
            "date_of_death": individual_details[6],
            "location": individual_details[7],
            "occupation": individual_details[8],
            "relation_type": individual_details[9]
        })
        individuals_list.append(individual)

    return individuals_list
