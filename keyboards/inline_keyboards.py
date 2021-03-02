"""
All inline keyboards
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

menu_cd = CallbackData("type", "amount", "currency")


async def show_currency_keyboard(amount):
    """
    The keyboard is formed from the types of currencies, if the user did not send the currency in the message
    :param amount:
    :return:
    """
    markup = InlineKeyboardMarkup()
    categories = ['tjs', 'rub', 'usd', 'eur']
    amount = amount.replace(",", ".")
    for category in categories:
        button_text = f"{amount} {category.upper()}"
        markup.row(
            InlineKeyboardButton(text=button_text,
                                 callback_data=menu_cd.new(amount=amount, currency=category))
        )
    return markup



