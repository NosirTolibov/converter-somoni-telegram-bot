"""Command handler coming from users"""
from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils import callback_data

from domain import get_news, parse_date, get_calculated_rate, get_nbt_rate, get_parsed_values
from keyboards.inline_keyboards import show_currency_keyboard, menu_cd
from loader import dp
from utils import exceptions, rate_limit


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Sends a welcome message"""
    await message.answer(
        f'Салом, {message.from_user.full_name}! 😊 🇹🇯\n'
        'Меня зовут Сомон.\n\n'
        f'<b>Вот что я умею.</b>\n'
        'Конвертер валют /help\n'
        '/nbt - Официальный курс Национального Банка Таджикистана\n'
        '/news - Новости экономики')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """Sends help via bot"""
    command_list = [
        f'<b>Список команд:</b>',
        '/start - Начать диалог',
        '/nbt - Официальный курс Национального Банка Таджикистана',
        '/news - Новости экономики\n',
        f'<b>Для ковертации валют, нужно отправить сообщение в формате:</b>',
        '- 500 рублей',
        '- 120.5 долларов',
        '- 354,95 евро',
        'или отправить сумму, а бот сам предложить вам тип валюты'
    ]
    await message.answer('\n'.join(command_list))


@dp.message_handler(commands=['news'])
async def send_news(message: types.Message):
    """Sends news randomly by tag National Bank of Tajikistan"""
    news_link = get_news()
    await message.answer(
        f'{news_link}')


# @rate_limit(120, 'nbt')
@dp.message_handler(commands=['nbt'])
async def national_bank_rate(message: types.Message):
    """Sends the rate of the National Bank of Tajikistan"""
    nbt_rate = get_nbt_rate()
    answer_message = f'<b>Официальные курсы валют к сомони:</b>\n' + \
                     '*по курсу НБТ за ' + parse_date(nbt_rate['date']) + '\n\n' + \
                     '🇷🇺 1 Рубль: ' + nbt_rate['rub'] + '\n' + \
                     '🇺🇸 1 Доллар: ' + nbt_rate['usd'] + '\n' + \
                     '🇪🇺 1 Евро: ' + nbt_rate['eur']
    await message.answer(answer_message)


@dp.message_handler(regexp='(^\d+(?:[\.,]\d+)?)$')
async def get_amount_for_converting(message: Union[CallbackQuery, Message]):
    """Accepts amount only a int or float type and shows a keyboard to select currency"""
    markup = await show_currency_keyboard(message.text)
    answer_message = f'Выберите валюту:'
    await message.answer(answer_message, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter())
async def send_converted_rate_keyboard(call: CallbackQuery, callback_data: dict):
    """
    Handles pressing in the currency keyboard (func: show_currency_keyboard)
    And returns converted results
    """
    amount = float(callback_data.get("amount"))
    currency = callback_data.get("currency")
    await call.message.edit_text(f'<b>{amount} {currency.upper()}</b>\n'
                                 f'{get_calculated_rate(amount, currency)}')


@dp.message_handler()
async def send_converted_rate(message: types.Message):
    """
    Processes sent messages such as amount and currency and returns the converted result
    Example: 500 рублей
    """
    try:
        expense = get_parsed_values(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f'<b>{expense.amount} {expense.currency_text.upper()}</b>\n'
        f'{get_calculated_rate(expense.amount, expense.currency_text)}')
    await message.answer(answer_message)
