from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

# ------------- Создаем клавиатуру через ReplyKeyboardBuilder -----------------

# Создаем кнопки для разбития товаров по категориям
medicines_button = KeyboardButton(text=LEXICON_RU['human_medicine'])
vet_medicines_button = KeyboardButton(text=LEXICON_RU['animals_medicine'])
medical_devices_button = KeyboardButton(text=LEXICON_RU['medical_devices'])
field_medicine_button = KeyboardButton(text=LEXICON_RU['field_medicine'])
standard_samples_button = KeyboardButton(text=LEXICON_RU['standard_samples'])

# Инициализируем билдер под все кнопки
categories_buttons = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер
categories_buttons.row(medicines_button, vet_medicines_button, medical_devices_button, field_medicine_button, standard_samples_button, width=2)

# Создаем клавиатуру с кнопками
categories_btns: ReplyKeyboardMarkup = categories_buttons.as_markup(
    one_timekeyboard=True,
    resize_keyboard=True
)

#-------------------- Inline Клавиатура ----------------------------

url_company_button = InlineKeyboardButton(
    text=LEXICON_RU['our_site'],
    url='https://endopharm.ru/company/'
)

inline_keyboard_url_company = InlineKeyboardMarkup(
    inline_keyboard=[[url_company_button]]
)

continue_button = InlineKeyboardButton(
    text=LEXICON_RU['continue_search']
)

inline_keyboard_continue_search = InlineKeyboardMarkup(
    inline_keyboard=[[continue_button]]
)