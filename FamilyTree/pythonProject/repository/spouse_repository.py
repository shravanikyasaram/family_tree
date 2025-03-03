from fastapi import HTTPException

from sqlalchemy import or_

from repository.individuals_entity import IndividualsEntity
from repository.marriage_entity import MarriageEntity


def get_spouse(spouse_id, db):
    return (db.query(IndividualsEntity, MarriageEntity)
            .join(MarriageEntity, or_(MarriageEntity.husband_id == IndividualsEntity.id,
                                      MarriageEntity.wife_id == IndividualsEntity.id))
            .filter(or_(MarriageEntity.husband_id == spouse_id,
                        MarriageEntity.wife_id == spouse_id))
            .filter(IndividualsEntity.id != spouse_id)
            .all())

def get_couple(couple_id, db):
    marriage = db.query(MarriageEntity).filter(MarriageEntity.id == couple_id).first()
    if not marriage:
        raise HTTPException(statucode=500, detail='No data found')

    husband = db.query(IndividualsEntity).filter(IndividualsEntity.id == marriage.husband_id).first()
    wife = db.query(IndividualsEntity).filter(IndividualsEntity.id == marriage.wife_id)

    return {
        "wedding_date": str(marriage.wedding_date),
        "husband": {
            "id": husband.id,
            "first_name": husband.first_name,
            "last_name": husband.last_name,
            "gender": husband.gender,
            "date_of_birth": str(husband.date_of_birth)
        },
        "wife": {
            "id": wife.id,
            "first_name": wife.first_name,
            "last_name": wife.last_name,
            "gender": wife.gender,
            "date_of_birth": str(wife.date_of_birth)
        }
    }
