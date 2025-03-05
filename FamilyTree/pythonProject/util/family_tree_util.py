from fastapi import HTTPException

from repository.individuals_repository import check_if_individual_already_exit


def check_if_user_already_exist(individuals, db):
    existing_individual = check_if_individual_already_exit(individuals, db)

    if existing_individual:
        raise HTTPException(status_code=500, detail='Individual already exist')