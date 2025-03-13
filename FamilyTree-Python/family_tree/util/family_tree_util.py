from fastapi import HTTPException

from repository.individuals_repository import check_if_individual_already_exit
from service.Logger import get_logger

logger = get_logger(__name__)

def check_if_user_already_exist(individual, db):
    existing_individual = check_if_individual_already_exit(individual, db)

    if existing_individual:
        raise HTTPException(status_code=500, detail='Individual already exist')