import os
from dotenv import load_dotenv
from pathlib import Path
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from utils.states import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from keyboards import inline
from utils import dicts, states

dotenv_path = Path('data/.env')
load_dotenv(dotenv_path=dotenv_path)

UID = os.getenv("Z_UID")

router = Router()


@router.message(Command("start"), StateFilter(default_state))
async def start(message: Message):
    """
    Обработчик команды /start

    Выводит сообщение "Привет, ник!"
    """
    await message.answer(f"Привет, {message.from_user.first_name}", reply_markup = inline.Kb_maker().callback_buttons(titles=["Отправить фанфик", "Отправить анкету"], callbacks=["connect", "soautor"], main_button = False, rows=2))

@router.message(Command("cancel"), ~StateFilter(default_state))
async def cancel_accept(message: Message, state: FSMContext):
    """
    Выход из машины состояния
    """
    await message.answer("Вы отменили действие!")
    await state.clear()
    await start(message)
    
@router.message(Command("cancel"))
async def incorrect_cancel(message: Message, state: FSMContext):
    """
    Попытка выхода из машины состояния, когда пользователь не находится в ней
    """
    await message.answer("Отменять нечего!")

@router.callback_query(F.data.in_("connect"), StateFilter(default_state))
async def connect_handler(callback: CallbackQuery, state: FSMContext):
    """
    Вход в машину состояний и вывод сообщения с указанием действий
    """
    await callback.message.answer(f"Отправь ссылку на Ваш фанфик или напиши /cancel для отмены.")
    await state.set_state(states.send_message.link)

@router.message(StateFilter(states.send_message.link), F.text)
async def link_handler(message: Message, state: FSMContext):
    """
    Ожидание текста(подразумевающего собой ссылку на фф), и перевод на следующую стадию - стадию отправки изображения
    """
    await state.update_data(user_name = message.from_user.first_name)
    await state.update_data(link = message.text)
    await message.answer(f"Теперь отправь обложку или любую понравившуюся картинку или напиши /cancel для отмены.")
    await state.set_state(states.send_message.image)

@router.message(StateFilter(states.send_message.link))
async def link_handler(message: Message):
    """
    Обработчик ошибки: попытка отправить не фотографию или видео.
    """
    await message.answer("Упс... что-то пошло не так. Пожалуйста, отправьте ссылку на фанфик еще раз или напишите /cancel для отмены.")

@router.message(StateFilter(states.send_message.image), F.photo | F.video)
async def image_handler(message: Message, state: FSMContext, bot: Bot):
    """
    Отправка готового фанфика администратору.
    """
    if message.photo:
        await state.update_data(image = message.photo[-1].file_id)
        await state.update_data(id = message.from_user.id)
        await message.answer(f"Фанфик успешно отправлен!")
        dicts.f_dict[message.from_user.id] = await state.get_data()
        await bot.send_photo(chat_id = UID, photo = dicts.f_dict[message.from_user.id]['image'],  caption = f"""Ник: `{dicts.f_dict[message.from_user.id]['user_name']}`
Ссылка: {dicts.f_dict[message.from_user.id]['link']}
Айди: `{dicts.f_dict[message.from_user.id]['id']}`""", parse_mode = "MARKDOWN", reply_markup = inline.Kb_maker().callback_buttons(["Ответить"], [str(dicts.f_dict[message.from_user.id]['id'])], main_button=False))
    if message.video:
        await state.update_data(video = message.video.file_id)
        await state.update_data(id = message.from_user.id)
        await message.answer(f"Фанфик успешно отправлен!")
        dicts.f_dict[message.from_user.id] = await state.get_data()
        await bot.send_video(chat_id = UID, video = dicts.f_dict[message.from_user.id]['video'],  caption = f"""Ник: `{dicts.f_dict[message.from_user.id]['user_name']}`
Ссылка: {dicts.f_dict[message.from_user.id]['link']}
Айди: `{dicts.f_dict[message.from_user.id]['id']}`""", parse_mode = "MARKDOWN", reply_markup = inline.Kb_maker().callback_buttons(["Ответить"], [str(dicts.f_dict[message.from_user.id]['id'])], main_button=False))
    dicts.f_dict.clear()
    await state.clear()
    await message.answer(f"Привет, {message.from_user.first_name}", reply_markup = inline.Kb_maker().callback_buttons(titles=["Отправить фанфик", "Отправить анкету"], callbacks=["connect", "soautor"], main_button = False, rows=2))


@router.message(StateFilter(states.send_message.image))
async def image_handler(message: Message):
    """
    обработчик ошибок: некорректная обложка
    """
    await message.answer("Упс... что-то пошло не так. Пожалуйста, отправьте обложку для фанфика еще раз или напишите /cancel для отмены.")


@router.callback_query(F.data == "answer_to_admin", StateFilter(default_state))
async def send_answer_to_admin_handler(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer(f"Введите сообщение для администратора или напишите /cancel для отмены.")
    await state.set_state(states.send_message.answer_to_admin)

@router.message(StateFilter(states.send_message.answer_to_admin))
async def send_answer_to_admin_handler(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(uid = message.from_user.id)
    if message.text:
        await state.update_data(message = message.text)
        dicts.f_dict[message.from_user.id] = await state.get_data()
        await bot.send_message(chat_id = UID, text = f"""Сообщение от пользователя с айди `{dicts.f_dict[message.from_user.id]['uid']}`

{message.text}""",  reply_markup = inline.Kb_maker().callback_buttons(["Ответить"], [str(dicts.f_dict[message.from_user.id]['uid'])], main_button=False), parse_mode = "MARKDOWN")
    if message.photo:
        await state.update_data(message = message.text)
        dicts.f_dict[message.from_user.id] = await state.get_data()
        await bot.send_photo(chat_id = UID, caption = f"Сообщение от пользователя с айди `{dicts.f_dict[message.from_user.id]['uid']}`" ,photo = message.photo[-1].file_id, reply_markup = inline.Kb_maker().callback_buttons(["Ответить"], [str(dicts.f_dict[message.from_user.id]['uid'])], main_button=False))
    if message.video:
        dicts.f_dict[message.from_user.id] = await state.get_data()
        await bot.send_video(chat_id = UID,caption = f"Сообщение от пользователя с айди `{dicts.f_dict[message.from_user.id]['uid']}`" , video = message.video.file_id, reply_markup = inline.Kb_maker().callback_buttons(["Ответить"], [str(dicts.f_dict[message.from_user.id]['uid'])], main_button=False))
    await message.answer(f"Сообщение успешно отправлено!")
    await state.clear()

@router.callback_query(StateFilter(default_state), F.data.regexp(r"^(\d+)$").as_("digits"))
async def answer_handler(callback: CallbackQuery, digits: int , state: FSMContext):
    await state.update_data(uid = digits[0])
    dicts.user_dict[callback.from_user.id] = await state.get_data()
    
    await callback.message.answer(f"""Введи сообщение для пользователя или напиши /cancel для отмены.""")
    await state.set_state(states.send_ans.message)



@router.message(StateFilter(states.send_ans.message), F.text | F.video | F.photo)
async def send_answer_to_user_handler(message: Message, state: FSMContext, bot: Bot):
    if message.text:
        await bot.send_message(chat_id = dicts.user_dict[message.from_user.id]['uid'], text = f"""Сообщение от администратора: 
{message.text}""", reply_markup = inline.answer_to_admin_kb())
    if message.photo:
        await bot.send_photo(chat_id = dicts.user_dict[message.from_user.id]['uid'],caption="Сообщение от администратора", photo = message.photo[-1].file_id, reply_markup = inline.answer_to_admin_kb())
    if message.video:
        await bot.send_video(chat_id = dicts.user_dict[message.from_user.id]['uid'],caption="Сообщение от администратора", video = message.video.file_id, reply_markup = inline.answer_to_admin_kb())
    await message.answer(f"Сообщение успешно отправлено!")
    await state.clear()

@router.message(StateFilter(states.send_answer.answer_to_user))
async def send_answer_to_user_handler(message: Message, state: FSMContext):
    await message.answer("Кто-то накосячил... Пожалуйста, введите сообщения для пользователя еще раз или напишите /cancel для отмены.")

@router.callback_query(F.data == "soautor")
async def profile(callback: CallbackQuery, state: FSMContext):
    await state.update_data(profile = callback.message.text)
    await callback.message.answer("Вставьте ссылку вашего профиля на фб или напишите /cancel для отмены.")
    await state.set_state(states.send_soautor.profile)

@router.message(StateFilter(states.send_soautor.profile), F.text)
async def soautor(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите, в качестве кого Вы отправляете анкету (бета/гамма/соавтор) или напишите /cancel для отмены.")
    await state.set_state(states.send_soautor.soautor)

@router.message(StateFilter(states.send_soautor.soautor), F.text)
async def ways(message: Message, state: FSMContext):
    await state.update_data(username = message.from_user.username)
    await state.update_data(soautor = message.text)
    await message.answer("Перечислите более предпочтительные для Вас направленности или напишите /cancel для отмены.")
    await state.set_state(states.send_soautor.marks)


@router.message(StateFilter(states.send_soautor.marks), F.text)
async def marks(message: Message, state: FSMContext):
    await state.update_data(ways = message.text)
    await message.answer("Перечислите предпочтительные работы с метками или напишите /cancel для отмены.")
    await state.set_state(states.send_soautor.anti_marks)


@router.message(StateFilter(states.send_soautor.anti_marks), F.text)
async def anti_marks(message: Message, state: FSMContext):
    await state.update_data(marks = message.text)
    await message.answer("Перечислите работы, с метками которых Вы не хотели бы работать или напишите /cancel для отмены.")
    await state.set_state(states.send_soautor.strong_sides)


@router.message(StateFilter(states.send_soautor.strong_sides), F.text)
async def strong_sides(message: Message, state: FSMContext):
    await state.update_data(anti_marks = message.text)
    await message.answer("Перечислите ваши сильные стороны или напишите /cancel для отмены.")
    await state.set_state(states.send_soautor.weak_sides)


@router.message(StateFilter(states.send_soautor.weak_sides), F.text)
async def weak_sides(message: Message, state: FSMContext):
    await state.update_data(strong_sides = message.text)
    await message.answer("Перечислите Ваши слабые стороны или напишите /cancel для отмены.")
    await state.set_state(states.send_soautor.expirience)


@router.message(StateFilter(states.send_soautor.expirience), F.text)
async def expirience(message: Message, state: FSMContext):
    await state.update_data(weak_sides = message.text)
    await message.answer("Напишите, был ли у Вас опыт работы или напишите /cancel для отмены.")
    await state.set_state(states.send_soautor.send)

@router.message(StateFilter(states.send_soautor.send), F.text)
async def send(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(expirience = message.text)
    dicts.soautor_dict[message.from_user.id] = await state.get_data()
    await message.answer("Анкета успешно отправлена!")
    await bot.send_message(UID, f"""Анкета:
                           
username: @{dicts.soautor_dict[message.from_user.id]['username']}
Роль: {dicts.soautor_dict[message.from_user.id]['soautor']}
Направленность: {dicts.soautor_dict[message.from_user.id]['ways']}
Метки: {dicts.soautor_dict[message.from_user.id]['marks']}
Анти-метки: {dicts.soautor_dict[message.from_user.id]['anti_marks']}
Сильные стороны: {dicts.soautor_dict[message.from_user.id]['strong_sides']}
Слабые стороны: {dicts.soautor_dict[message.from_user.id]['weak_sides']}
Опыт: {dicts.soautor_dict[message.from_user.id]['expirience']}""", reply_markup=inline.Kb_maker().callback_buttons(["Ответить"], [f"{message.from_user.id}"], main_button=False))
    await state.clear()

