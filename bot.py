from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommand

from keyboards.keyboards import categories_btns, inline_keyboard

from lexicon.lexicon_ru import LEXICON_RU

from environs import Env

import asyncio

env = Env()
env.read_env()

bot_token = env('bot_token')

from scraping.scraping import search_medicines, search_vet_medicines, search_medical_devices, search_field_medicines, search_standard_samples

# Создаем объекты бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher()

# Хранилице данных пользователя, (в теории можно переделать в @dataclass)
users = {}

# ----------------- Обработчики апдейтов -----------------

# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=categories_btns
    )
    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'category': None
        }


# Этот хендлер отвечает на команду "info"
# Отправляет инструкцию для работы с ботом
@dp.message(Command(commands='info'))
async def process_info_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/info'],
        reply_markup=inline_keyboard
    )


# Этот хэндлер будет срабатывать на ответ "Лекарственные препараты"
@dp.message(F.text == 'Лекарственные препараты')
async def process_state_medicines(message: Message):
    await message.answer(
        text='Введите свой запрос...'
    )

    users[message.from_user.id]['category'] = 'Лекарственные препараты'
    print(users[message.from_user.id]['category'])


# Этот хэндлер будет срабатывать на ответ "Лекарственные препараты"
@dp.message(lambda message: users[message.from_user.id]['category'] == 'Лекарственные препараты')
async def process_searching_products(message: Message):
    products = await search_medicines(message.text.lower().split())
    text = 'По вашему запросу найдено:\n'
    i = 0
    for values, keys in products.items():
        i += 1
        text += f'{i}. {keys}: {values}\n'
        if i == 15:
            break
    await message.answer(text=text)


# Этот хэндлер будет срабатывать на ответ "Ветеринария"
@dp.message(F.text == 'Ветеринария')
async def process_state_vet_medicines(message: Message):
    await message.answer(
        text='Введите свой запрос...'
    )
    users[message.from_user.id]['category'] = 'Ветеринария'


# Этот хэндлер будет срабатывать на ответ "Ветеринария"
@dp.message(lambda message: users[message.from_user.id]['category'] == 'Ветеринария')
async def process_searching_vet_products(message: Message):
    products = await search_vet_medicines(message.text.lower().split())
    text = 'По вашему запросу найдено:\n'
    i = 0
    for values, keys in products.items():
        i += 1
        text += f'{i}. {keys}: {values}\n'
        if i == 15:
            break
    await message.answer(text=text)


# Этот хэндлер будет срабатывать на ответ "Медицинские изделия"
@dp.message(F.text == 'Медицинские изделия')
async def process_state_med_devices(message: Message):
    await message.answer(
        text='Введите свой запрос...'
    )
    users[message.from_user.id]['category'] = 'Медицинские изделия'


# Этот хэндлер будет срабатывать на ответ "Медицинские изделия"
@dp.message(lambda message: users[message.from_user.id]['category'] == 'Медицинские изделия')
async def process_searching_medical_devices(message: Message):
    products = await search_medical_devices(message.text.lower().split())
    text = 'По вашему запросу найдено:\n'
    i = 0
    for values, keys in products.items():
        i += 1
        text += f'{i}. {keys}: {values}\n'
        if i == 15:
            break
    await message.answer(text=text)


# Этот хэндлер будет срабатывать на ответ "Тактическая медицина"
@dp.message(F.text == 'Тактическая медицина')
async def process_state_med_devices(message: Message):
    await message.answer(
        text='Введите свой запрос...'
    )
    users[message.from_user.id]['category'] = 'Тактическая медицина'


# Этот хэндлер будет срабатывать на ответ "Тактическая медицина"
@dp.message(lambda message: users[message.from_user.id]['category'] == 'Тактическая медицина')
async def process_searching_field_medicines(message: Message):
    products = await search_field_medicines(message.text.lower().split())
    text = 'По вашему запросу найдено:\n'
    i = 0
    for values, keys in products.items():
        i += 1
        text += f'{i}. {keys}: {values}\n'
        if i == 15:
            break
    await message.answer(text=text)


# Этот хэндлер будет срабатывать на ответ "Стандартные образцы"
@dp.message(F.text == 'Стандартные образцы')
async def process_state_med_devices(message: Message):
    await message.answer(
        text='Введите свой запрос...'
    )
    users[message.from_user.id]['category'] = 'Стандартные образцы'


# Этот хэндлер будет срабатывать на ответ "Стандартные образцы"
@dp.message(lambda message: users[message.from_user.id]['category'] == 'Стандартные образцы')
async def process_searching_standard_samples(message: Message):
    products = await search_standard_samples(message.text.lower().split())

    text = 'По вашему запросу найдено:\n'
    i = 0
    for values, keys in products.items():
        i += 1
        text += f'{i}. {keys}: {values}\n'
        if i == 15:
            break
    await message.answer(text=text)


# Меню команд
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Команда запуска бота'),
        BotCommand(command='/info', description='Инофрмация о работе бота')
    ]

    await bot.set_my_commands(main_menu_commands)

# Регистрируем асинхронную функцию в диспетчере,
# которая будет выполняться на старте бота,
dp.startup.register(set_main_menu)


if __name__ == '__main__':
    dp.run_polling(bot)