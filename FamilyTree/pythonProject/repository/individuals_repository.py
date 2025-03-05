from sqlalchemy import text

from Model.individuals import Individuals
from repository.individuals_entity import IndividualsEntity


def find_by_individuals_id(individuals_id, db):
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

def get_family_tree(individuals_id, db):
    query = text("""with recursive family_tree as
        (
        select i.id AS individual_id, i.first_name, i.last_name, i.gender,
                i.date_of_birth, i.date_of_death, i.location, i.occupation, NULL as relation_type, NULL as related_id
        from individuals i where i.id = :individuals_id
        
        UNION ALL
        
        select i.id AS individual_id, i.first_name, i.last_name, i.gender,
                i.date_of_birth, i.date_of_death, i.location, i.occupation,
                'parent' as relation_type, p.child_id as related_id
        from individuals i JOIN parent_child p on (i.id = p.father_id OR i.id = p.mother_id)
        where p.child_id = :individuals_id
        
        UNION ALL
        
        select i.id AS individual_id, i.first_name, i.last_name, i.gender,
                i.date_of_birth, i.date_of_death, i.location, i.occupation,
                'spouse' as relation_type, m.id as related_id
        from individuals i join marriage m on i.id = m.husband_id or i.id = m.wife_id
        where m.husband_id = :individuals_id or m.wife_id = :individuals_id
        
        union all
        
        select i.id AS individual_id, i.first_name, i.last_name, i.gender,
                i.date_of_birth, i.date_of_death, i.location, i.occupation,
                'child' as relation_type, pc.father_id as related_id
        from individuals i join parent_child pc on i.id = pc.child_id
        where pc.father_id = :individuals_id or pc.mother_id = :individuals_id
            )
        select * from family_tree""")

    result = db.execute(query, {"individuals_id": individuals_id})
    family_tree = result.fetchall()
    return family_tree

def check_if_individual_already_exit(individuals, db):
    existing_individual = db.query(IndividualsEntity).filter(
        IndividualsEntity.first_name == individuals["first_name"],
        IndividualsEntity.last_name == individuals["last_name"],
        IndividualsEntity.date_of_birth == individuals["date_of_birth"]).first()
