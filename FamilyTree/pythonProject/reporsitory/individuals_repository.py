from reporsitory.individuals_entity import IndividualsEntity


def find_by_individuals_id(individuals_id, db):
    return db.query(IndividualsEntity).filter(IndividualsEntity.id == individuals_id).first()
