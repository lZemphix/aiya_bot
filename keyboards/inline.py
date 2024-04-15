from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_kb():
    connect = InlineKeyboardButton(text="Отправить фанфик", callback_data="connect")
    start = InlineKeyboardMarkup(inline_keyboard=[[connect]])
    return start

def answer_to_user_kb():
    answer = InlineKeyboardButton(text="Ответить", callback_data="answer_to_user")
    answer_kb = InlineKeyboardMarkup(inline_keyboard=[[answer]])
    return answer_kb

def answer_to_admin_kb():
    answer = InlineKeyboardButton(text="Ответить", callback_data="answer_to_admin")
    answer_to_admin_kb = InlineKeyboardMarkup(inline_keyboard=[[answer]])
    return answer_to_admin_kb