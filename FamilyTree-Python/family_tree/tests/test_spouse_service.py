from datetime import date
from unittest.mock import MagicMock

from fastapi import HTTPException

import pytest

from Model.individuals import Individuals
from Model.partner import Partner
from Model.spouse import Spouse
from service.spouse_service import get_spouse_details, add_new_spouse


def test_get_spouse_details_no_data(mocker):
    mocker.patch('service.spouse_service.get_spouse', return_value = [])

    with pytest.raises(HTTPException) as e:
        get_spouse_details(1, db=None)

    assert e.value.status_code == 200
    assert e.value.detail == 'No details found'

def test_get_spouse_details(mocker):
    mock_spouse_id = 1
    mock_spouse = Individuals(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950,1,2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')

    mock_spouse_data = Partner(**mock_spouse.__dict__, wedding_date=date(1980,1,2))
    mock_data = [(mock_spouse, mock_spouse_data)]
    mocker.patch('service.spouse_service.get_spouse', return_value = mock_data)

    result = get_spouse_details(mock_spouse_id, db=None)

    assert result[0]["spouse"]["first_name"] == 'John'
    assert result[0]["wedding_date"] == date(1980,1,2)

def test_get_spouse_details_multiple_wives(mocker):
    mock_spouse_id = 1
    mock_spouse_one = Individuals(first_name='Jane', last_name='Doe', nick_name='JD', date_of_birth=date(1950,1,2),
                             date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')
    mock_spouse_two = Individuals(first_name='Alice', last_name='Doe', nick_name='AD', date_of_birth=date(1951, 1, 2),
                              date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')

    mock_spouse_data_one = Partner(**mock_spouse_one.__dict__, wedding_date=date(1985,1,2))
    mock_spouse_data_two = Partner(**mock_spouse_two.__dict__, wedding_date=date(1980,1,2))

    mock_data = [(mock_spouse_one, mock_spouse_data_one), (mock_spouse_two, mock_spouse_data_two)]
    mocker.patch('service.spouse_service.get_spouse', return_value = mock_data)

    result = get_spouse_details(mock_spouse_id, db=None)

    assert result[0]["spouse"]["first_name"] == 'Jane'
    assert result[0]["wedding_date"] == date(1985,1,2)
    assert result[1]["spouse"]["first_name"] == 'Alice'
    assert result[1]["wedding_date"] == date(1980, 1, 2)

def test_add_spouse_with_no_individual_id(mocker):
    mock_spouse = Individuals(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950, 1, 2),
                              date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')

    mock_spouse_data = Partner(**mock_spouse.__dict__, wedding_date=date(1980, 1, 2))
    mock_data = Spouse(individual_id=1, partner=[mock_spouse_data])

    mock_db = MagicMock()
    mocker.patch('service.spouse_service.get_by_individuals_id', return_value=None)

    with pytest.raises(HTTPException) as e:
        add_new_spouse(mock_data, db=mock_db)

    assert e.value.status_code == 500
    assert e.value.detail == 'Invalid Spouse details'

def test_add_spouse_check_if_user_already_exist(mocker):
    mock_spouse = Individuals(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950, 1, 2),
                              date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')

    mock_spouse_data = Partner(**mock_spouse.__dict__, wedding_date=date(1980, 1, 2))
    mock_data = Spouse(individual_id=1, partner=[mock_spouse_data])

    mock_partner_details = Individuals(first_name='Jane', last_name='Doe', nick_name='JD',
                                       date_of_birth=date(1955, 1, 2),
                                       date_of_death=date(1995, 1, 2), occupation='Doctor', gender='Female', location='CA')

    mock_db = MagicMock()
    mocker.patch('service.spouse_service.get_by_individuals_id', return_value=mock_partner_details)
    mocker.patch('util.family_tree_util.check_if_user_already_exist', return_value=mock_spouse)

    with pytest.raises(HTTPException) as e:
        add_new_spouse(mock_data, db=mock_db)

    assert e.value.status_code == 500
    assert e.value.detail == 'Individual already exist'

def test_add_spouse(mocker):
    mock_spouse = Individuals(first_name='John', last_name='Doe', nick_name='JD', date_of_birth=date(1950, 1, 2),
                              date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Male', location='CA')

    mock_spouse_data = Partner(**mock_spouse.__dict__, wedding_date=date(1980, 1, 2))
    mock_data = Spouse(individual_id=1, partner=[mock_spouse_data])

    mock_partner_details = Individuals(first_name='Jane', last_name='Doe', nick_name='JD',
                                       date_of_birth=date(1955, 1, 2),
                                       date_of_death=date(1995, 1, 2), occupation='Doctor', gender='Female',
                                       location='CA')

    mock_db = MagicMock()
    mocker.patch('service.spouse_service.get_by_individuals_id', return_value=mock_partner_details)
    mocker.patch('service.spouse_service.check_if_user_already_exist', return_value=None)

    result = add_new_spouse(mock_data, mock_db)

    args, kwargs = mock_db.add.call_args_list[1]

    assert mock_db.add.call_count == 2
    assert mock_db.add.call_args_list[0][0][0].first_name == 'John'
    assert args[0].wedding_date == date(1980, 1, 2)

def test_add_multiple_spouses(mocker):
    mock_spouse_one = Individuals(first_name='Jane', last_name='Doe', nick_name='JD', date_of_birth=date(1950, 1, 2),
                              date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Female', location='CA')

    mock_spouse_data_one = Partner(**mock_spouse_one.__dict__, wedding_date=date(1980, 1, 2))

    mock_spouse_two = Individuals(first_name='Alice', last_name='C', nick_name='AC', date_of_birth=date(1950, 1, 2),
                              date_of_death=date(2025, 1, 1), occupation='Doctor', gender='Female', location='CA')

    mock_spouse_data_two = Partner(**mock_spouse_two.__dict__, wedding_date=date(1990, 1, 2))

    mock_partner_details = Individuals(first_name='John', last_name='Doe', nick_name='JD',
                                       date_of_birth=date(1955, 1, 2),
                                       date_of_death=date(1995, 1, 2), occupation='Doctor', gender='Male',
                                       location='CA')

    mock_data = Spouse(individual_id=1, partner=[mock_spouse_data_one, mock_spouse_data_two])

    mock_db = MagicMock()
    mocker.patch('service.spouse_service.get_by_individuals_id', return_value=mock_partner_details)
    mocker.patch('service.spouse_service.check_if_user_already_exist', return_value=None)

    result = add_new_spouse(mock_data, db=mock_db)

    args, kwargs = mock_db.add.call_args_list[0]
    args_one, kwargs_one = mock_db.add.call_args_list[1]
    args_two, kwargs = mock_db.add.call_args_list[2]
    args_three, kwargs_one = mock_db.add.call_args_list[3]

    assert mock_db.add.call_count == 4
    assert args[0].first_name == 'Jane'
    assert args_two[0].first_name == 'Alice'
    assert args_one[0].wedding_date == date(1980, 1, 2)
    assert args_three[0].wedding_date == date(1990, 1, 2)
