from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

class send_message(StatesGroup):
    link = State()
    image = State()
    answer_to_admin = State()
    
class send_answer(StatesGroup):
    id = State()
    answer_to_user = State()

class send_ans(StatesGroup):
    message = State()

class send_soautor(StatesGroup):
    soautor = State()
    ways = State()
    marks = State()
    anti_marks = State()
    strong_sides = State()
    weak_sides = State()
    expirience = State()
    send = State()
