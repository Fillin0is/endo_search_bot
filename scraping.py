import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch(url, session):
    headers = {
        "Accept": "text/html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    }
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def parse_product_info(url, session):
    html = await fetch(url, session)
    soup = BeautifulSoup(html, 'lxml')
    info_product = soup.find_all('div', class_='content')
    ar = [line for info in info_product for line in info.stripped_strings]
    return url, [item.lower() for item in ar if item != '']

async def search_medicines(search_terms):
    url_medicines = "https://endopharm.ru/product/lekarstvennye-preparaty/"
    async with aiohttp.ClientSession() as session:
        html = await fetch(url_medicines, session)
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.find_all('a', class_='colored')

        medicine = [parse_product_info(f'https://endopharm.ru{quote.get("href")}', session) for quote in quotes]
        med_products_info = await asyncio.gather(*medicine)

        count = 0

        found_keys = set()
        found_products = {}
        for key, value in med_products_info:
            if any(term in s for term in search_terms for s in value):
                if key not in found_keys:
                    count += 1
                    found_products[key] = value[0]
                    found_keys.add(key)
        
        if count == 0:
            return '\nПродукция по данному запросу не была найдена, проверьте правильность написанного запроса, либо данная продукция не производится на нашем предприятии'
        else:
            return found_products


async def search_vet_medicines(search_terms):
    url_vet_medicines = "https://endopharm.ru/product/veterinariya/"
    async with aiohttp.ClientSession() as session:
        html = await fetch(url_vet_medicines, session) 
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.select('.text .dark-color')

        vet_medicine = [parse_product_info(f'https://endopharm.ru{quote.get("href")}', session) for quote in quotes]
        vet_products_info = await asyncio.gather(*vet_medicine)

        count = 0

        found_keys = set()
        found_products = {}
        for key, value in vet_products_info:
            if any(term in s for term in search_terms for s in value):
                if key not in found_keys:
                    count += 1
                    found_products[key] = value[0]
                    found_keys.add(key)
        
        if count == 0:
            return '\nПродукция по данному запросу не была найдена, проверьте правильность написанного запроса, либо данная продукция не производится на нашем предприятии'
        else:
            return found_products
        
async def search_medical_devices(search_terms):
    url_medical_devices = "https://endopharm.ru/product/meditsinskie-izdeliya/"
    async with aiohttp.ClientSession() as session:
        html = await fetch(url_medical_devices, session) 
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.select('.text .dark-color')

        vet_medicine = [parse_product_info(f'https://endopharm.ru{quote.get("href")}', session) for quote in quotes]
        vet_products_info = await asyncio.gather(*vet_medicine)

        count = 0

        found_keys = set()
        found_products = {}
        for key, value in vet_products_info:
            if any(term in s for term in search_terms for s in value):
                if key not in found_keys:
                    count += 1
                    found_products[key] = value[0]
                    found_keys.add(key)
        
        if count == 0:
            return '\nПродукция по данному запросу не была найдена, проверьте правильность написанного запроса, либо данная продукция не производится на нашем предприятии'
        else:
            return found_products
        

async def search_field_medicines(search_terms):
    url_tactical_medicines = "https://endopharm.ru/product/takticheskaya-meditsina/"
    async with aiohttp.ClientSession() as session:
        html = await fetch(url_tactical_medicines, session) 
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.select('.text .dark-color')

        vet_medicine = [parse_product_info(f'https://endopharm.ru{quote.get("href")}', session) for quote in quotes]
        vet_products_info = await asyncio.gather(*vet_medicine)

        count = 0

        found_keys = set()
        found_products = {}
        for key, value in vet_products_info:
            if any(term in s for term in search_terms for s in value):
                if key not in found_keys:
                    count += 1
                    found_products[key] = value[0]
                    found_keys.add(key)
        
        if count == 0:
            return '\nПродукция по данному запросу не была найдена, проверьте правильность написанного запроса, либо данная продукция не производится на нашем предприятии'
        else:
            return found_products
        

async def search_standard_samples(search_terms):
    url_standard_samples = "https://endopharm.ru/product/standartnye-obraztsy/"
    async with aiohttp.ClientSession() as session:
        html = await fetch(url_standard_samples, session) 
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.select('.text .dark-color')

        standard_samples = [parse_product_info(f'https://endopharm.ru{quote.get("href")}', session) for quote in quotes]
        standard_samples_info = await asyncio.gather(*standard_samples)

        count = 0

        found_keys = set()
        found_products = {}
        for key, value in standard_samples_info:
            if any(term in s for term in search_terms for s in value):
                if key not in found_keys:
                    count += 1
                    found_products[key] = value[0]
                    found_keys.add(key)
        print(found_products)

        
        if count == 0:
            return '\nПродукция по данному запросу не была найдена, проверьте правильность написанного запроса, либо данная продукция не производится на нашем предприятии'
        else:
            return found_products