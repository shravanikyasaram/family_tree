from sqlalchemy import text

from repository.individuals_entity import IndividualsEntity


def get_by_individuals_id(individuals_id, db):
    return db.query(IndividualsEntity).filter(IndividualsEntity.id == individuals_id).first()

def get_individual_id_by_last_name(last_name, db):
    query = text("""select i.id from individuals i
        left join parent_child pc on i.id = pc.child_id
        where i.last_name = :last_name
        and pc.child_id is null
        order by i.date_of_birth
        limit 1""")
    result = db.execute(query, {"last_name": last_name}).scalar()
    return result

def get_individual(individual_id, db):
    query = text("""select * from individuals where id = :individual_id""")
    result = db.execute(query, {"individual_id": individual_id}).fetchone()
    return result._asdict() if result else None

def get_spouse_details(individual_id, db):
    query = text("""SELECT i.*, m.wedding_date
        FROM marriage m
        JOIN individuals i
        ON (m.husband_id = i.id OR m.wife_id = i.id)
        WHERE (m.husband_id = :individual_id OR m.wife_id = :individual_id)
          AND i.id != :individual_id""")
    result = db.execute(query, {"individual_id": individual_id}).fetchall()
    return [row._asdict() for row in result]

def get_children_details(parent_id, spouse_id, db):
    query = text("""SELECT *
        FROM individuals
        WHERE id IN (
            SELECT child_id FROM parent_child
            WHERE (father_id = :parent_id AND mother_id = :spouse_id)
               OR (father_id = :spouse_id AND mother_id = :parent_id))
        """)
    result = db.execute(query, {"parent_id": parent_id, "spouse_id": spouse_id}).fetchall()
    return [row._asdict() for row in result]

def check_if_individual_already_exit(individual, db):
    existing_user = db.query(IndividualsEntity).filter(
        IndividualsEntity.first_name == individual["first_name"],
        IndividualsEntity.last_name == individual["last_name"],
        IndividualsEntity.date_of_birth == individual["date_of_birth"]).first()
    return existing_user
