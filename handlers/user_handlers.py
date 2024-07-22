from aiogram import F 
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommand
from aiogram import Router

from keyboards.keyboards import categories_btns, inline_keyboard

from lexicon.lexicon_ru import LEXICON_RU

from scraping.scraping import search_medicines, search_vet_medicines, search_medical_devices, search_field_medicines, search_standard_samples

# ----------------- Обработчики апдейтов -----------------

users = {}

router = Router()

# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@router.message(CommandStart())
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
@router.message(Command(commands='info'))
async def process_info_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/info'],
        reply_markup=inline_keyboard
    )


# Этот хэндлер будет срабатывать на ответ "Лекарственные препараты"
@router.message(F.text == LEXICON_RU['human_medicine'])
async def process_state_medicines(message: Message):
    await message.answer(
        text = LEXICON_RU['write_request']
    )
    users[message.from_user.id]['category'] = LEXICON_RU['human_medicine']


# Этот хэндлер будет срабатывать на ответ "Лекарственные препараты"
@router.message(lambda message: users[message.from_user.id]['category'] == LEXICON_RU['human_medicine'])
async def process_searching_products(message: Message):
    products_message = await search_medicines(message.text.lower().split())
    text = LEXICON_RU['find_answer']
    i = 0
    if type(products_message) == dict:
        for values, keys in products_message.items():
            i += 1
            text += f'{i}. {keys}: {values}\n'
            if i == 15:
                break
    else:
        text = products_message
        
    users[message.from_user.id]['category'] = ''
    await message.answer(text=text)


# Этот хэндлер будет срабатывать на ответ "Ветеринария"
@router.message(F.text == LEXICON_RU['animals_medicine'])
async def process_state_vet_medicines(message: Message):
    await message.answer(
        text=LEXICON_RU['write_request']
    )
    users[message.from_user.id]['category'] = LEXICON_RU['animals_medicine']


# Этот хэндлер будет срабатывать на ответ "Ветеринария"
@router.message(lambda message: users[message.from_user.id]['category'] == LEXICON_RU['animals_medicine'])
async def process_searching_vet_products(message: Message):
    products_message = await search_vet_medicines(message.text.lower().split())
    text = LEXICON_RU['find_answer']
    i = 0
    if type(products_message) == dict:
        for values, keys in products_message.items():
            i += 1
            text += f'{i}. {keys}: {values}\n'
            if i == 15:
                break
    else:
        text = products_message
        
    users[message.from_user.id]['category'] = ''
    await message.answer(text=text)



# Этот хэндлер будет срабатывать на ответ "Медицинские изделия"
@router.message(F.text == LEXICON_RU['medical_devices'])
async def process_state_med_devices(message: Message):
    await message.answer(
        text=LEXICON_RU['write_request']
    )
    users[message.from_user.id]['category'] = LEXICON_RU['medical_devices']


# Этот хэндлер будет срабатывать на ответ "Медицинские изделия"
@router.message(lambda message: users[message.from_user.id]['category'] == LEXICON_RU['medical_devices'])
async def process_searching_medical_devices(message: Message):
    products_message = await search_medical_devices(message.text.lower().split())
    text = LEXICON_RU['find_answer']
    i = 0
    if type(products_message) == dict:
        for values, keys in products_message.items():
            i += 1
            text += f'{i}. {keys}: {values}\n'
            if i == 15:
                break
    else:
        text = products_message
        
    users[message.from_user.id]['category'] = ''
    await message.answer(text=text)



# Этот хэндлер будет срабатывать на ответ "Тактическая медицина"
@router.message(F.text == LEXICON_RU['field_medicine'])
async def process_state_med_devices(message: Message):
    await message.answer(
        text = LEXICON_RU['write_request']
    )
    users[message.from_user.id]['category'] = LEXICON_RU['field_medicine']


# Этот хэндлер будет срабатывать на ответ "Тактическая медицина"
@router.message(lambda message: users[message.from_user.id]['category'] == LEXICON_RU['field_medicine'])
async def process_searching_field_medicines(message: Message):
    products_message = await search_field_medicines(message.text.lower().split())
    text = LEXICON_RU['find_answer']
    i = 0
    if type(products_message) == dict:
        for values, keys in products_message.items():
            i += 1
            text += f'{i}. {keys}: {values}\n'
            if i == 15:
                break
    else:
        text = products_message
        
    users[message.from_user.id]['category'] = ''
    await message.answer(text=text)



# Этот хэндлер будет срабатывать на ответ "Стандартные образцы"
@router.message(F.text == LEXICON_RU['standard_samples'])
async def process_state_med_devices(message: Message):
    await message.answer(
        text = LEXICON_RU['write_request']
    )
    users[message.from_user.id]['category'] = LEXICON_RU['standard_samples']


# Этот хэндлер будет срабатывать на ответ "Стандартные образцы"
@router.message(lambda message: users[message.from_user.id]['category'] == LEXICON_RU['standard_samples'])
async def process_searching_standard_samples(message: Message):
    products_message = await search_standard_samples(message.text.lower().split())

    text = LEXICON_RU['find_answer']
    i = 0
    if type(products_message) == dict:
        for values, keys in products_message.items():
            i += 1
            text += f'{i}. {keys}: {values}\n'
            if i == 15:
                break
    else:
        text = products_message
        
    users[message.from_user.id]['category'] = ''
    await message.answer(text=text)