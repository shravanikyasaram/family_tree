from datetime import date

from repository.children_repository import get_children
from repository.individuals_entity import IndividualsEntity


def test_get_children(mocker):
    mock_db = mocker.MagicMock()

    dummy_individual = IndividualsEntity(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950,1,2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')

    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_filter = mock_join.filter.return_value
    mock_filter.all.return_value = [dummy_individual]

    result = get_children(1, db=mock_db)

    assert result == [dummy_individual]
    mock_db.query.assert_called_once_with(IndividualsEntity)

def test_get_children_no_data(mocker):
    mock_db = mocker.MagicMock()
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_filter = mock_join.filter.return_value
    mock_filter.all.return_value = []

    result = get_children(1, db=mock_db)

    assert result == []
    mock_db.query.assert_called_once_with(IndividualsEntity)