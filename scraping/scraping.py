import aiohttp
import asyncio
from bs4 import BeautifulSoup

from lexicon.lexicon_ru import LEXICON_RU

# -------------------------------------
async def fetch(url, session):
    headers = {
        "Accept": "text/html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    }
    async with session.get(url, headers=headers) as response:
        return await response.text()


# --------------------------------
async def parse_product_info(url, session):
    html = await fetch(url, session)
    soup = BeautifulSoup(html, 'lxml')
    info_product = soup.find_all('div', class_='content')
    ar = [line for info in info_product for line in info.stripped_strings]
    return url, [item.lower() for item in ar if item != '']

# -------------------------------
async def parse_h1(url, session):
    html = await fetch(url, session)
    soup = BeautifulSoup(html, 'lxml')
    h1 = soup.find('h1').text.strip()
    return h1

# Функция парсинга лекарственных препаратов
cache_medicines = {}

async def search_medicines(search_terms):
    global cache_medicines
    
    if cache_medicines != {}:
        found_products = {}
        count = 0
        for key, value in cache_medicines.items():
            if any(word in i for word in search_terms for i in value[1].lower().split() if len(word) >= 3):
                count += 1
                found_products[key] = value[1]
            if any(term in s for term in search_terms for s in value[0] if len(term) >= 3): 
                count += 1
                found_products[key] = value[1]

        if count == 0:
            return LEXICON_RU['no_find_products']
        else:
            return found_products
    
    url_medicines = "https://endopharm.ru/product/lekarstvennye-preparaty/"
    async with aiohttp.ClientSession() as session:
        html = await fetch(url_medicines, session)
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.find_all('a', class_='colored')

        # Проверяем, какие ссылки уже есть в кэше
        existing_links = set(cache_medicines.keys())
        new_links = [f'https://endopharm.ru{quote.get("href")}' for quote in quotes if f'https://endopharm.ru{quote.get("href")}' not in existing_links]

        # Парсим только новые ссылки
        medicine = [parse_product_info(link, session) for link in new_links]
        med_products_info = await asyncio.gather(*medicine)

        # Дополнительный парсинг заголовка h1 для новых ссылок
        for key, value in med_products_info:
            h1 = await parse_h1(key, session)
            value_cache = (value, h1)  # Добавление заголовка h1 в кортеж с данными
            cache_medicines[key] = value_cache  # Добавляем данные в кэш


        count = 0
        found_products = {}
        for key, value in cache_medicines.items():
            if any(word in i for word in search_terms for i in value[1].lower().split() if len(word) >= 3):
                count += 1
                found_products[key] = value[1]
            if any(term in s for term in search_terms for s in value[0] if len(term) >= 3): 
                count += 1
                found_products[key] = value[1]

        if count == 0:
            return LEXICON_RU['no_find_products']
        else:
            return found_products


# Функция парсинга ветеринарной продукции
cache_vet_medicines = {}

async def search_vet_medicines(search_terms):
    global cache_vet_medicines

    if cache_vet_medicines != {}:
        found_products = {}
        count = 0
        for key, value in cache_vet_medicines.items():
            if any(word in i for word in search_terms for i in value[1].lower().split() if len(word) >= 3):
                count += 1
                found_products[key] = value[1]
            if any(term in s for term in search_terms for s in value[0] if len(term) >= 3): 
                count += 1
                found_products[key] = value[1]

        if count == 0:
            return LEXICON_RU['no_find_products']
        else:
            return found_products

    url_vet_medicines = "https://endopharm.ru/product/veterinariya/"
    async with aiohttp.ClientSession() as session:
        html = await fetch(url_vet_medicines, session) 
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.select('.text .dark-color')

        # Проверяем, какие ссылки уже есть в кэше
        existing_links = set(cache_vet_medicines.keys())
        new_links = [f'https://endopharm.ru{quote.get("href")}' for quote in quotes if f'https://endopharm.ru{quote.get("href")}' not in existing_links]

        # Парсим только новые ссылки
        vet_medicine = [parse_product_info(link, session) for link in new_links]
        vet_products_info = await asyncio.gather(*vet_medicine)

        # Дополнительный парсинг заголовка h1 для новых ссылок
        for key, value in vet_products_info:
            h1 = await parse_h1(key, session)
            value_cache = (value, h1)  # Добавление заголовка h1 в кортеж с данными
            cache_vet_medicines[key] = value_cache  # Добавляем данные в кэш

        count = 0
        found_products = {}
        for key, value in cache_vet_medicines.items():
            if any(word in i for word in search_terms for i in value[1].lower().split() if len(word) >= 3):
                count += 1
                found_products[key] = value[1]
            if any(term in s for term in search_terms for s in value[0] if len(term) >= 3): 
                count += 1
                found_products[key] = value[1]
        
        if count == 0:
            return LEXICON_RU['no_find_products']
        else:
            return found_products


# Функция парсинга медицинский изделий
cache_medical_devices = {}

async def search_medical_devices(search_terms):
    global cache_medical_devices

    if cache_medical_devices != {}:
        count = 0
        found_products = {}
        for key, value in cache_medical_devices.items():
            if any(word in i for word in search_terms for i in value[1].lower().split() if len(word) >= 3):
                count += 1
                found_products[key] = value[1]
            if any(term in s for term in search_terms for s in value[0] if len(term) >= 3): 
                count += 1
                found_products[key] = value[1]
        
        if count == 0:
            return LEXICON_RU['no_find_products']
        else:
            return found_products

    url_medical_devices = "https://endopharm.ru/product/meditsinskie-izdeliya/"
    async with aiohttp.ClientSession() as session:
        html = await fetch(url_medical_devices, session) 
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.select('.text .dark-color')

        medical_devices_products_info = []

        medical_devices = [parse_product_info(f'https://endopharm.ru{quote.get("href")}', session) for quote in quotes]
        medical_devices_products_info.extend(await asyncio.gather(*medical_devices))

        pagen = [link['href'] for link in soup.find('ul', class_='pagination').find_all('a')]
        pagen = pagen[0:-1]  # Спаршенные ссылки на страницы с пагинацией, убираем последнюю ссылку

        base_url = 'https://endopharm.ru'

        for link in pagen:
            html = await fetch(f'{base_url}{link}', session)
            soup = BeautifulSoup(html, 'lxml')
            quotes = soup.select('.text .dark-color')

            # Парсим информацию о медицинских изделиях на текущей странице
            medical_devices = [parse_product_info(f'https://endopharm.ru{quote.get("href")}', session) for quote in quotes]
            medical_devices_products_info.extend(await asyncio.gather(*medical_devices))

        for key, value in medical_devices_products_info:
            h1 = await parse_h1(key, session)  # Получаем заголовок h1 для каждого продукта
            value_with_h1 = (value, h1)  # Добавляем заголовок h1 к данным о продукте
            cache_medical_devices[key] = value_with_h1  # Добавляем данные в кэш

        count = 0
        found_products = {}
        for key, value in cache_medical_devices.items():
            if any(word in i for word in search_terms for i in value[1].lower().split() if len(word) >= 3):
                count += 1
                found_products[key] = value[1]
            if any(term in s for term in search_terms for s in value[0] if len(term) >= 3): 
                count += 1
                found_products[key] = value[1]
        
        if count == 0:
            return LEXICON_RU['no_find_products']
        else:
            return found_products
        

# Функция парсинга изделий такстической медицины
cache_field_medicines = {}

async def search_field_medicines(search_terms):
    global cache_field_medicines

    if cache_field_medicines != {}:
        found_products = {}
        count = 0
        for key, value in cache_field_medicines.items():
            if any(word in i for word in search_terms for i in value[1].lower().split() if len(word) >= 3):
                count += 1
                found_products[key] = value[1]
            if any(term in s for term in search_terms for s in value[0] if len(term) >= 3): 
                count += 1
                found_products[key] = value[1]

        if count == 0:
            return LEXICON_RU['no_find_products']
        else:
            return found_products

    url_tactical_medicines = "https://endopharm.ru/product/takticheskaya-meditsina/"
    async with aiohttp.ClientSession() as session:
        html = await fetch(url_tactical_medicines, session) 
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.select('.text .dark-color')
        
        # Проверяем, какие ссылки уже есть в кэше
        existing_links = set(cache_field_medicines.keys())
        new_links = [f'https://endopharm.ru{quote.get("href")}' for quote in quotes if f'https://endopharm.ru{quote.get("href")}' not in existing_links]

        # Парсим только новые ссылки
        tactical_medicine = [parse_product_info(link, session) for link in new_links]
        tactical_products_info = await asyncio.gather(*tactical_medicine)

        for key, value in tactical_products_info:
            h1 = await parse_h1(key, session)
            value_cache = (value, h1)  # Добавление заголовка h1 в кортеж с данными
            cache_field_medicines[key] = value_cache  # Добавляем данные в кэш

        count = 0
        found_products = {}
        for key, value in cache_field_medicines.items():
            if any(word in i for word in search_terms for i in value[1].lower().split() if len(word) >= 3):
                count += 1
                found_products[key] = value[1]
            if any(term in s for term in search_terms for s in value[0] if len(term) >= 3): 
                count += 1
                found_products[key] = value[1]
        
        if count == 0:
            return LEXICON_RU['no_find_products']
        else:
            return found_products
        

# Функция парсинга стандартных образцов препаратов
cache_standard_samples = {}

async def search_standard_samples(search_terms):
    global cache_standard_samples

    if cache_standard_samples != {}:
        count = 0
        found_products = {}
        for key, value in cache_standard_samples.items():
            if any(word in i for word in search_terms for i in value[1].lower().split() if len(word) >= 3):
                count += 1
                found_products[key] = value[1]
            if any(term in s for term in search_terms for s in value[0] if len(term) >= 3): 
                count += 1
                found_products[key] = value[1]

        if count == 0:
            return LEXICON_RU['no_find_products']
        else:
            return found_products

    url_standard_samples = "https://endopharm.ru/product/standartnye-obraztsy/"
    
    async with aiohttp.ClientSession() as session:
        html = await fetch(url_standard_samples, session) 
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.select('.text .dark-color')

        standard_samples_info = []

        # Парсим информацию о стандартных образцах на первой странице
        standard_samples = [parse_product_info(f'https://endopharm.ru{quote.get("href")}', session) for quote in quotes]
        standard_samples_info.extend(await asyncio.gather(*standard_samples))

        pagen = [link['href'] for link in soup.find('ul', class_='pagination').find_all('a')]
        pagen = pagen[0:-1] # Спаршенные ссылки на страницы с пагинацией, убираем последнюю ссылку

        base_url = 'https://endopharm.ru'

        for link in pagen:
            html = await fetch(f'{base_url}{link}', session)
            soup = BeautifulSoup(html, 'lxml')
            quotes = soup.select('.text .dark-color')

            # Парсим информацию о стандартных образцах на текущей странице
            standard_samples = [parse_product_info(f'https://endopharm.ru{quote.get("href")}', session) for quote in quotes]
            standard_samples_info.extend(await asyncio.gather(*standard_samples))

        for key, value in standard_samples_info:
            h1 = await parse_h1(key, session)  # Получаем заголовок h1 для каждого продукта
            value_with_h1 = (value, h1)  # Добавляем заголовок h1 к данным о продукте
            cache_standard_samples[key] = value_with_h1  # Добавляем данные в кэш

        count = 0
        found_products = {}
        for key, value in cache_standard_samples.items():
            if any(word in i for word in search_terms for i in value[1].lower().split() if len(word) >= 3):
                count += 1
                found_products[key] = value[1]
            if any(term in s for term in search_terms for s in value[0] if len(term) >= 3): 
                count += 1
                found_products[key] = value[1]
        
        if count == 0:
            return LEXICON_RU['no_find_products']
        else:
            return found_products