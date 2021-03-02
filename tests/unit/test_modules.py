import pytest
from domain import parse_date, get_parsed_values

from domain.module import Message, calculate_rate


@pytest.mark.skip
@pytest.mark.parametrize("date,expected", [('20210525', '25-05-2021'), ('20200128', '28-01-2020'),
                                           ('20191231', '31-12-2019')])
def test_parse_date(date, expected):
    assert parse_date(date) == expected


@pytest.mark.skip
def test_get_parsed_values():
    assert get_parsed_values('200 сомони') == Message(amount=200.0, currency_text='tjs')
    assert get_parsed_values('152,69 рублей') == Message(amount=152.69, currency_text='rub')
    assert get_parsed_values('623459,90 долларов') == Message(amount=623459.90, currency_text='usd')
    assert get_parsed_values('1500000 евро') == Message(amount=1500000, currency_text='eur')


@pytest.mark.skip
def test_calculate_rate():
    assert calculate_rate(200.0, 'tjs', 'rub', 'usd', 'eur') == \
           {'date': '20210303', 'eur': '14.69', 'rub': '1309.76', 'usd': '17.69'}

