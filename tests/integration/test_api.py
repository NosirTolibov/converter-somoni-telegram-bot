import pytest
import requests

from loader import API_NBT_EXCHANGE_RATE


@pytest.mark.skip()
def test_api_nbt_exchange_rate():
    r = requests.get(API_NBT_EXCHANGE_RATE)
    http_status = r.status_code
    assert http_status == 200
    if http_status == 200:
        response = r.json()
        assert sorted(list(response.keys())) == sorted(['date', 'rub', 'eur', 'usd'])

