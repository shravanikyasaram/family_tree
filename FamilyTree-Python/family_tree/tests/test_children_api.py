from datetime import date

from repository.individuals_entity import IndividualsEntity
from repository.parent_child_entity import ParentChildEntity


def test_get_children(client, test_db):
    father = IndividualsEntity(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950,1,2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')
    mother = IndividualsEntity(first_name='Jane', last_name='Doe', nick_name='JD', date_of_birth=date(1950, 1, 2),
                               date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')
    test_db.add_all([father, mother])
    test_db.commit()
    test_db.refresh(father)
    test_db.refresh(mother)

    child = IndividualsEntity(first_name='Alice', last_name='Doe', nick_name='AD', date_of_birth=date(1970,1,2),
                             date_of_death=None, occupation='Doctor', gender='Male', location='CA')

    test_db.add_all([child])
    test_db.commit()
    test_db.refresh(child)

    test_db.add_all([
        ParentChildEntity(father_id=father.id, child_id=child.id, mother_id=mother.id)
    ])
    test_db.commit()

    response = client.get(f'/children/{father.id}')
    assert response.status_code == 200
    result = response.json()
    assert result[0]['first_name'] == 'Alice'

