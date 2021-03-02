"""Functions"""
import requests
import re
import logging
import datetime
import random
from bs4 import BeautifulSoup
from typing import NamedTuple, Dict

from loader import API_NBT_EXCHANGE_RATE

from utils import ApiResponseException, NotCorrectMessage

logger = logging.getLogger()

CURRENCY_TEXT_OPTIONS = {'сомони': 'tjs', 'сомон': 'tjs', 'сом': 'tjs', 'tj': 'tjs', 'tjs': 'tjs', 'somoni': 'tjs',
                         'som': 'tjs', 's': 'tjs', '$': 'usd', 'доллар': 'usd', 'долар': 'usd', 'долларов': 'usd',
                         'дол': 'usd', 'usd': 'usd', 'us': 'usd', 'dollar': 'usd', 'dollars': 'usd', 'бакс': 'usd',
                         'баксов': 'usd', '₽': 'rub', 'рубль': 'rub', 'рублей': 'rub', 'руб': 'rub', 'рубл': 'rub',
                         'ru': 'rub', 'rub': 'rub', 'rus': 'rub', 'ruble': 'rub', 'rubles': 'rub', 'rouble': 'rub',
                         'roubles': 'rub', '€': 'eur', 'евро': 'eur', 'евра': 'eur', 'eu': 'eur', 'eur': 'eur',
                         'euro': 'eur', 'euros': 'eur'}
CURRENCY_SIGN = {
    'tjs': '🇹🇯 Сомони',
    'rub': '🇷🇺 Рубль',
    'usd': '🇺🇸 Доллар',
    'eur': '🇪🇺 Евро'}

TJS = 'tjs'
RUB = 'rub'
USD = 'usd'
EUR = 'eur'


class Message(NamedTuple):
    """Structure of a parsed currency conversion message"""
    amount: float
    currency_text: str


def get_nbt_rate() -> Dict:
    """
    Makes API request and shows the exchange rate of National Bank of Tajikistan
    :return:
    """
    try:
        # r = requests.get('https://httpbin.org/status/400')
        r = requests.get(API_NBT_EXCHANGE_RATE)
        r.raise_for_status()
    except Exception as e:
        ApiResponseException(e)
        return
    response = r.json()
    return response


def get_parsed_values(raw_message: str) -> Message:
    """
    Parsing a message and identifying the type of currency
    :param raw_message:
    :return:
    """
    parse_message = _parse_message(raw_message)
    currency_name = _get_currency(parse_message.currency_text)
    return Message(amount=parse_message.amount, currency_text=currency_name)


def calculate_rate(amount: float, currency: str, *args: str) -> Dict:
    """
    Currency conversions
    :param amount:
    :param currency:
    :param args:
    :return:
    """
    rate_dict = get_nbt_rate()
    tjs_rate = amount
    calculated_rate = {'date': rate_dict['date']}
    # cur_dict = {cur: "{:.2f}".format(float(amount))}
    if currency != TJS:
        tjs_rate = amount * float(rate_dict[currency])
    for item in args:
        if item != TJS:
            calculated_rate[item] = "{:.2f}".format(float(tjs_rate) / float(rate_dict[item]))
        else:
            calculated_rate[item] = "{:.2f}".format(amount * float(rate_dict[currency]))
    return calculated_rate


def get_calculated_rate(amount: float, currency: str) -> str:
    """
    Bring the converted rate dict into a single message form
    :param amount:
    :param currency:
    :return:
    """
    rate = {}
    if currency == TJS:
        rate = calculate_rate(amount, currency, RUB, USD, EUR)
    elif currency == RUB:
        rate = calculate_rate(amount, currency, TJS, USD, EUR)
    elif currency == USD:
        rate = calculate_rate(amount, currency, TJS, RUB, EUR)
    elif currency == EUR:
        rate = calculate_rate(amount, currency, TJS, RUB, USD)
    rate_list = [f'{CURRENCY_SIGN[key]}: {value}' for key, value in rate.items() if key != 'date']
    return (f'по курсу НБТ за {parse_date(rate["date"])}\n\n' +
            f'\n'.join(rate_list))


def _get_currency(currency_name: str) -> str:
    """
    Defining currency type by message text
    :param currency_name:
    :return:
    """
    try:
        return CURRENCY_TEXT_OPTIONS[currency_name]
    except KeyError:
        raise NotCorrectMessage(
            "Не могу отпределить валюты. Напишите в сообщение после суммы следующие валюты: "
            "\nсомони, рубль, доллар и евро")


def _parse_message(raw_message: str) -> Message:
    """
    Parsing message text for amount and currency
    :param raw_message:
    :return:
    """
    regexp_result = re.match(r"(\d+(?:[\.,]\d+)?) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n1300 сомони")
    amount = float(regexp_result.group(1).replace(" ", "").replace(",", "."))
    currency_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, currency_text=currency_text)


def parse_date(date: str) -> str:
    """
    Changing date format from YYYYMMDD to DD-MM-YYYY
    :param date:
    :return:
    """
    date_format = datetime.datetime.strptime(date, '%Y%m%d')
    return date_format.strftime('%d-%m-%Y')


def get_news() -> str:
    """
    Parsing news web page and get random one actual article url
    :return:
    """
    url_news_domain = f'https://tj.sputniknews.ru'
    url_news = f'{url_news_domain}/tags/organization_Nacionalnyjj_bank_Tadzhikistana/'
    headers = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'accept': '*/*'
    }
    try:
        r = requests.get(url_news, headers=headers)
        r.raise_for_status()
    except Exception as e:
        ApiResponseException(e)
        return
    soap = BeautifulSoup(r.content, 'html.parser')
    tableList = soap.find_all('h2', class_='b-plainlist__title')
    url_list = [f"{url_news_domain}{link.find('a')['href']}" for link in tableList]
    return random.choice(url_list)

