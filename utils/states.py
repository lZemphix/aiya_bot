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
