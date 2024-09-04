import executor
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API = ''
bot = Bot(token=API)
DP = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать калории')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)


@DP.message_handler(commands=['start'])
async def buttons(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=kb)


class UserState(StatesGroup):
    weight = State()
    growth = State()
    age = State()


@DP.message_handler(text=['Рассчитать калории'])
async def set_age(message):
    await message.answer('Введите свой возраст.')
    await UserState.age.set()


@DP.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(user_age=message.text)
    await message.answer('Введите свой рост.')
    await UserState.growth.set()


@DP.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(user_growth=message.text)
    await message.answer('Введите свой вес.')
    await UserState.weight.set()


@DP.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(user_weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['user_weight'])) + (6.25 * int(data['user_growth'])) - ((5 * int(data['user_age'])) + 5)
    await message.answer(f'Ваша норма калорий: {result}')
    await state.finish()


@DP.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(DP, skip_updates=True)