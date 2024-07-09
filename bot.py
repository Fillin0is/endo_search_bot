from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from scraping import search_medicines, search_vet_medicines, search_medical_devices, search_field_medicines, search_standard_samples


# Данные для токена берутся из области вижимости окружения
bot_token = '7098586282:AAFmf52ohep5DUcGN-kpfMtvk5BChe2UAsw'

# Создаем объекты бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher()

# Хранилице данных пользователя, (в теории можно переделать в @dataclass)
users = {}

# ------------- Создаем клавиатуру через ReplyKeyboardBuilder -----------------

# Создаем кнопки для разбития товаров по категориям
medicines_button = KeyboardButton(text='Лекарственные препараты')
vet_medicines_button = KeyboardButton(text='Ветеринария')
medical_devices_button = KeyboardButton(text='Медицинские изделия')
field_medicine_button = KeyboardButton(text='Тактическая медицина')
standard_samples_button = KeyboardButton(text='Стандартные образцы')

# Инициализируем билдер под все кнопки
categories_buttons = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер
categories_buttons.row(medicines_button, vet_medicines_button, medical_devices_button, field_medicine_button, standard_samples_button, width=2)

# Создаем клавиатуру с кнопками
categories_btns: ReplyKeyboardMarkup = categories_buttons.as_markup(
    one_timekeyboard=True,
    resize_keyboard=True
)

url_company_button = InlineKeyboardButton(
    text='Наш сайт',
    url='https://endopharm.ru/company/'
)

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[url_company_button]]
)

# ----------------- Обработчики апдейтов -----------------

# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Добро пожаловать!\n\nЭтот бот предназначен для удобного поиска медицинских товаров, от всеразличных препаратов до медицинский инструментов\n\nДля подробной инструкции о работе бота нажмите на /info\n\nТакже вы можете охнакомиться с нашей компанией более подробно, перейдя на наш сайт',
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
        text='Для использования бота необходимо знать пару деталей:\n\n1) Поиск бота организован по категориям медицинских продуктов, производимых компанией, для выбора одной из категории необходимо выбрать эту категорию из появившихся кнопок внизу экрана\n\n2) После выбора категории товара, необходимо вписать и отправить запрос боту, который может содеражть как название товара, так и примерное его описание\n\n3) Исходя из ващего запроса будут найдены товары с похожим описанием, в ваш чат будут отправлены ссылки на товары, через которые вы сможете подробнее ознакомиться с продукцией\n\nТакже ниже под этим сообщением расположена кнопка, которая переведет вас на наш сайт, где вы можете узнать о нас чуточку больше!',
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
    print(message.text)
    products = await search_medicines(message.text.lower().split())
    print(products)
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
    print(users[message.from_user.id]['category'])


# Этот хэндлер будет срабатывать на ответ "Ветеринария"
@dp.message(lambda message: users[message.from_user.id]['category'] == 'Ветеринария')
async def process_searching_vet_products(message: Message):
    print(message.text)
    products = await search_vet_medicines(message.text.lower().split())
    print(products)
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
    print(users[message.from_user.id]['category'])


# Этот хэндлер будет срабатывать на ответ "Медицинские изделия"
@dp.message(lambda message: users[message.from_user.id]['category'] == 'Медицинские изделия')
async def process_searching_medical_devices(message: Message):
    print(message.text)
    products = await search_medical_devices(message.text.lower().split())
    print(products)
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
    print(users[message.from_user.id]['category'])


# Этот хэндлер будет срабатывать на ответ "Тактическая медицина"
@dp.message(lambda message: users[message.from_user.id]['category'] == 'Тактическая медицина')
async def process_searching_field_medicines(message: Message):
    print(message.text)
    products = await search_field_medicines(message.text.lower().split())
    print(products)
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
    print(users[message.from_user.id]['category'])


# Этот хэндлер будет срабатывать на ответ "Стандартные образцы"
@dp.message(lambda message: users[message.from_user.id]['category'] == 'Стандартные образцы')
async def process_searching_standard_samples(message: Message):
    print(message.text)
    products = await search_standard_samples(message.text.lower().split())

    print(type(products))

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