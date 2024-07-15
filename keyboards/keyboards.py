from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU


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

#-------------------- Inline Клавиатура ----------------------------

url_company_button = InlineKeyboardButton(
    text='Наш сайт',
    url='https://endopharm.ru/company/'
)

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[url_company_button]]
)
