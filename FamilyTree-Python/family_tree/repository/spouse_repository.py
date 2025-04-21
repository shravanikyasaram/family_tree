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

def get_couple(individual_id, db):
    marriage = db.query(MarriageEntity).filter(or_(MarriageEntity.husband_id == individual_id,
                                               MarriageEntity.wife_id == individual_id)).first()
    if not marriage:
        raise HTTPException(status_code=500, detail='No marriage details found')

    husband_details = db.query(IndividualsEntity).filter(IndividualsEntity.id == marriage.husband_id).first()
    wife_details = db.query(IndividualsEntity).filter(IndividualsEntity.id == marriage.wife_id).first()

    return marriage, husband_details, wife_details
