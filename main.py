import requests
import time
from bs4 import BeautifulSoup
from random import randrange

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36'
}


def get_page(url):
    """Функція що збирає всі посилання на категорії"""
    r = requests.session()
    response = r.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    services_link = soup.find('div', class_="js-services-maps").find_all('a', href=True)[0:11]
    services_link_list = []

    for sl in services_link:
        sl_url = sl.get('href')
        # print(sl_url)
        services_link_list.append(sl_url)

    with open('services_link.txt', 'w') as file:
        for url in services_link_list:
            file.write(f'https://list.in.ua{url}\n')

    return 'Зібрав усі посилання'


def get_services_phones_number(file_path):
    try:
        """Функція що збирає всі номери телефонів з категорії"""
        with open(file_path) as file:
            urls_list = [line.strip() for line in file.readlines()]

        r = requests.session()
        for url in urls_list:
            time.sleep(randrange(1, 4))
            response = r.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            """ шукаємо кількість сторінок """
            try:
                pagination_count = int(soup.find('div', class_='pagination-sunshine').find_all('a')[-1].text)
            except:
                print("Лиш одна сторінка")
            # print(pagination_count)
            """ проходимось по кожній сторінці, підставивши цифру сторінки в ссилку """
            for page in range(1, pagination_count + 1):
                time.sleep(randrange(1, 4))
                phone_number_list = []
                response = r.get(url=f'{url}/page/{page}', headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                print(f'Обробив {page}/{pagination_count}')
                phone_number = soup.find_all('a', class_='js-store-user-action-statistic')

                for pn in phone_number:
                    """ записуємо номери в список """
                    the_num = pn.get('data-adtext')
                    phone_number_list.append(the_num)

                with open(f'phones.txt', 'a+') as file:
                    for pns in phone_number_list:
                        file.write(f'{pns}\n')
    except:
        print('Файл не знайдено, або посилання не правильне')


def main():
    get_page('https://list.in.ua/%D0%86%D0%B2%D0%B0%D0%BD%D0%BE-%D0%A4%D1%80%D0%B0%D0%BD%D0%BA%D1%96%D0%B2%D1%81%D1%8C%D0%BA')
    get_services_phones_number('services_link.txt')


if __name__ == '__main__':
    main()

