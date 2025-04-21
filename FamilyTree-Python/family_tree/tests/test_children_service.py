from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock

from fastapi import HTTPException

import pytest

from Model.children import Children
from Model.individuals import Individuals
from service.children_service import get_children_details, add_children


def test_get_children(mocker):
    mock_data = [Individuals(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950,1,2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA'),
                 Individuals(first_name='Jane', last_name='Doe', nick_name='JD', date_of_birth=date(1948, 1, 2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Female', location='CA')
                 ]

    mocker.patch("service.children_service.get_children", return_value = mock_data)
    result = get_children_details(2, db=None)
    assert result[0].first_name == 'Jane'
    assert result[1].first_name == 'John'

def test_get_children_with_no_children_found(mocker):
    mocker.patch('service.children_service.get_children', return_value = [])

    with pytest.raises(HTTPException) as e:
        get_children_details(1, db=None)

    assert e.value.status_code == 500
    assert e.value.detail == 'No children details found'

def test_get_children_twins(mocker):
    mock_data = [Individuals(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950,1,2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA'),
                 Individuals(first_name='Jane', last_name='Doe', nick_name='JD', date_of_birth=date(1950, 1, 2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Female', location='CA')
                 ]

    mocker.patch('service.children_service.get_children', return_value = mock_data)
    result = get_children_details(1, db=None)
    assert result[0].first_name == 'John'
    assert result[1].first_name == 'Jane'

def test_add_children_with_no_parent_id():
    child = Individuals(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950,1,2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')
    mock_data = SimpleNamespace(
        children = [child],
        father_id = None,
        mother_id = None
    )

    with pytest.raises(HTTPException) as e:
        add_children(mock_data, db=None)

    assert e.value.status_code == 400
    assert e.value.detail == 'Invalid Children details.'

def test_add_children(mocker):
    child = Individuals(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950,1,2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')

    mock_data = Children(
        children = [child],
        father_id = 1,
        mother_id = 2)

    mock_db = MagicMock()
    mocker.patch('service.children_service.check_if_user_already_exist', return_value=None)
    result = add_children(mock_data, db=mock_db)

    assert mock_db.add.call_count == 2
    assert mock_db.add.call_args_list[0][0][0].first_name == 'John'
    assert mock_db.add.call_args_list[1][0][0].father_id == 1

def test_add_children_user_already_exist(mocker):
    child = Individuals(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950,1,2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')

    mock_data = Children(
        children = [child],
        father_id = 1,
        mother_id = 2)

    mock_db = MagicMock()
    mocker.patch('util.family_tree_util.check_if_user_already_exist', return_value=child)

    with pytest.raises(HTTPException) as e:
        add_children(mock_data, mock_db)

    assert e.value.status_code == 500
    assert e.value.detail == 'Individual already exist'
