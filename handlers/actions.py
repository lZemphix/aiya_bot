from keyboards import inline
from utils import states
from data import desc
from data.config import UID 
from utils import dicts


async def start_message(message):
    await message.answer(f"""{desc.start(message)}""", reply_markup = inline.start_kb() )
    
async def connect_action(message, state):
    await message.answer(f"Отправь ссылку на Ваш фанфик или напиши /cancel для отмены.")
    await state.set_state(states.send_message.link)

async def link_action(message, state):
    await state.update_data(user_name = message.from_user.first_name)
    await state.update_data(link = message.text)
    await message.answer(f"Теперь отправь обложку или любую понравившуюся картинку или напиши /cancel для отмены.")
    await state.set_state(states.send_message.image)

async def image_action(message, state, bot):
    if message.photo:
        await state.update_data(image = message.photo[-1].file_id)
        await state.update_data(id = message.from_user.id)
        await message.answer(f"Фанфик успешно отправлен!")
        dicts.f_dict[message.from_user.id] = await state.get_data()
        await bot.send_photo(chat_id = UID[0], photo = dicts.f_dict[message.from_user.id]['image'],  caption = f"""Ник: `{dicts.f_dict[message.from_user.id]['user_name']}`
Ссылка: {dicts.f_dict[message.from_user.id]['link']}
Айди: `{dicts.f_dict[message.from_user.id]['id']}`""", parse_mode = "MARKDOWN", reply_markup = inline.answer_to_user_kb())
    if message.video:
        await state.update_data(video = message.video.file_id)
        await state.update_data(id = message.from_user.id)
        await message.answer(f"Фанфик успешно отправлен!")
        dicts.f_dict[message.from_user.id] = await state.get_data()
        await bot.send_video(chat_id = UID[0], video = dicts.f_dict[message.from_user.id]['video'],  caption = f"""Ник: `{dicts.f_dict[message.from_user.id]['user_name']}`
Ссылка: {dicts.f_dict[message.from_user.id]['link']}
Айди: `{dicts.f_dict[message.from_user.id]['id']}`""", parse_mode = "MARKDOWN", reply_markup = inline.answer_to_user_kb())
    dicts.f_dict.clear()
    await state.clear()
    await start_message(message)


async def answer_action(callback, state):
    await callback.message.answer(f"""Введите айди пользователя или напиши /cancel для отмены """)
    await state.set_state(states.send_answer.id)

async def uid_action(message, state):
    await state.update_data(uid = message.text)
    dicts.user_dict[message.from_user.id] = await state.get_data()
    await message.answer(f"Введи сообщения для пользователя или напиши /cancel для отмены.")
    await state.set_state(states.send_answer.answer_to_user)

async def send_answer_to_user_action(message, state, bot):
    if message.text:
        await bot.send_message(chat_id = dicts.user_dict[message.from_user.id]['uid'], text = f"""Сообщение от администратора: 
{message.text}""", reply_markup = inline.answer_to_admin_kb())
    if message.photo:
        await bot.send_photo(chat_id = dicts.user_dict[message.from_user.id]['uid'],caption="Сообщение от администратора", photo = message.photo[-1].file_id, reply_markup = inline.answer_to_admin_kb())
    if message.video:
        await bot.send_video(chat_id = dicts.user_dict[message.from_user.id]['uid'],caption="Сообщение от администратора", video = message.video.file_id, reply_markup = inline.answer_to_admin_kb())
    await message.answer(f"Сообщение успешно отправлено!")
    await state.clear()

async def send_answer_to_admin_action(callback, state):
    await callback.message.delete()
    await callback.message.answer(f"Введите сообщение для администратора или напишите /cancel для отмены.")
    await state.set_state(states.send_message.answer_to_admin)

async def send_answer_to_admin_action2(message, state, bot):
    if message.text:
        await state.update_data(message = message.text)
        await state.update_data(uid = message.from_user.id)
        dicts.f_dict[message.from_user.id] = await state.get_data()
        await bot.send_message(chat_id = UID[0], text = f"""Сообщение от пользователя с айди `{dicts.f_dict[message.from_user.id]['uid']}`

{message.text}""", reply_markup = inline.answer_to_user_kb(), parse_mode = "MARKDOWN")
    if message.photo:
        await bot.send_photo(chat_id = UID[0], caption = f"Сообщение от пользователя с айди `{dicts.f_dict[message.from_user.id]['uid']}`" ,photo = message.photo[-1].file_id, reply_markup = inline.answer_to_user_kb(), parse_mode = "MARKDOWN")
    if message.video:
        await bot.send_video(chat_id = UID[0],caption = f"Сообщение от пользователя с айди `{dicts.f_dict[message.from_user.id]['uid']}`" , video = message.video.file_id, reply_markup = inline.answer_to_user_kb(), parse_mode = "MARKDOWN")
    await message.answer(f"Сообщение успешно отправлено!")
    await state.clear()