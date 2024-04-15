from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram import Bot
from handlers.actions import *
from utils.states import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
router = Router()

# Стартовая панель
@router.message(Command("start"), StateFilter(default_state))
async def start(message: Message):
    await start_message(message)

@router.message(Command("cancel"), ~StateFilter(default_state))
async def cancel_accept(message: Message, state: FSMContext):
    await message.answer("Вы отменили действие!")
    await state.clear()
    
@router.message(Command("cancel"))
async def incorrect_cancel(message: Message, state: FSMContext):
    await message.answer("Отменять нечего!")

@router.callback_query(F.data.in_("connect"), StateFilter(default_state))
async def connect_handler(callback: CallbackQuery, state: FSMContext):
    await connect_action(callback.message, state)

@router.message(StateFilter(states.send_message.link), F.text)
async def link_handler(message: Message, state: FSMContext):
    await link_action(message, state)

@router.message(StateFilter(states.send_message.link))
async def link_handler(message: Message):
    await message.answer("Упс... что-то пошло не так. Пожалуйста, отправьте ссылку на фанфик еще раз или напишите /cancel для отмены.")

@router.message(StateFilter(states.send_message.image), F.photo | F.video)
async def image_handler(message: Message, state: FSMContext, bot: Bot):
    await image_action(message, state, bot)

@router.message(StateFilter(states.send_message.image))
async def image_handler(message: Message):
    await message.answer("Упс... что-то пошло не так. Пожалуйста, отправьте обложку для фанфика еще раз или напишите /cancel для отмены.")


@router.callback_query(F.data == "answer_to_user", StateFilter(default_state))
async def answer_handler(callback: CallbackQuery, bot: Bot , state: FSMContext):
    await answer_action(callback, state)

@router.message(StateFilter(states.send_answer.id), F.text)
async def uid_handler(message: Message, state: FSMContext):
    await uid_action(message, state)

@router.message(StateFilter(states.send_answer.id))
async def uid_handler(message: Message):
    await message.answer("Что-то явно пошло не по плану... Пожалуйста, введите айди пользователя еще раз или напишите /cancel для отмены.")

@router.message(StateFilter(states.send_answer.answer_to_user), F.text | F.video | F.photo)
async def send_answer_to_user_handler(message: Message, state: FSMContext, bot: Bot):
    await send_answer_to_user_action(message, state, bot)

@router.message(StateFilter(states.send_answer.answer_to_user))
async def send_answer_to_user_handler(message: Message):
    await message.answer("Кто-то накосячил... Пожалуйста, введите сообщения для пользователя еще раз или напишите /cancel для отмены.")

@router.callback_query(F.data == "answer_to_admin", StateFilter(default_state))
async def send_answer_to_admin_handler(callback: CallbackQuery, state: FSMContext):
    await send_answer_to_admin_action(callback, state)

@router.message(StateFilter(states.send_message.answer_to_admin))
async def send_answer_to_admin_handler(message: Message, state: FSMContext, bot: Bot):
    await send_answer_to_admin_action2(message, state, bot)