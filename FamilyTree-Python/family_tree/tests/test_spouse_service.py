from datetime import date

from fastapi import HTTPException

import pytest

from Model.individuals import Individuals
from Model.partner import Partner
from Model.spouse import Spouse
from service.spouse_service import get_spouse_details


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
