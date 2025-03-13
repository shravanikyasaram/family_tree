from fastapi import HTTPException

from repository.individuals_entity import IndividualsEntity
from repository.individuals_repository import get_individual_id_by_last_name, get_individual, get_spouse_details, \
    get_children_details
from repository.marriage_entity import MarriageEntity
from service.Logger import get_logger
from util.family_tree_util import check_if_user_already_exist

logger = get_logger(__name__)

def add_first_couple(individuals, db):
    if not individuals.husband or not individuals.wife:
        raise HTTPException(status_code=400, detail='You have to enter both Husband and Wife details.')

    husband_details = individuals.husband.model_dump()
    husband = IndividualsEntity()
    check_if_user_already_exist(husband_details, db)

    db.add(husband)
    db.flush()
    logger.info("Saving husband details: %s",  husband)

    for wife_data in individuals.wife:
        wife_details = wife_data.model_dump()
        wedding_date = wife_details.pop("wedding_date")
        check_if_user_already_exist(wife_details, db)
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
        raise HTTPException(status_code=500, detail='No family members found')

    individual = get_individual(individual_id, db)
    family_tree = build_family_tree(individual, db)

    return family_tree


def build_family_tree(individual, db):
    individual_id = individual['id']
    spouses = get_spouse_details(individual_id, db)
    children = []

    for spouse in spouses:
        spouse_children = get_children_details(individual_id, spouse["id"], db)
        spouse["children"] = []

        for child in spouse_children:
            child_data = get_individual(child["id"], db)
            spouse["children"].append(build_family_tree(child_data, db))
            children.append(build_family_tree(child_data, db))

    family_tree = {
        **individual
    }

    if spouses:
        family_tree["spouse"] = spouses

    return family_tree