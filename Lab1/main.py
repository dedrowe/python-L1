import csv
import requests
import json
import logging


def write_value_to_file(value: tuple) -> None:
    """
    Функция записывает данные в таблицу

    value: строка которая будет записана в таблицу
    """
    try:
        with open("dataset.csv", 'a') as dataset:
            writer = csv.writer(dataset, dialect='unix')
            writer.writerow(value)
    except OSError:
        logging.warning("Ошибка открытия файла")


def parse_value(valute: str, min_date: str = '1992-07-01', source: str = 'https://www.cbr-xml-daily.ru/daily_json.js'):
    """
    Функция получает данные с сайта до последней записи

    valute: валюта, значение которой программа будет извлекать
    min_date: дата последней записи
    source: ссылка на запись
    """
    page_code = requests.get(source)
    d_page_code = json.loads(page_code.text)

    while True:
        page_code = requests.get("https:" + d_page_code['PreviousURL'])
        write_value_to_file((d_page_code['Date'][:10], d_page_code["Valute"][valute]['Value']))
        d_page_code = json.loads(page_code.text)
        if d_page_code['Date'][:10] == min_date:
            write_value_to_file((d_page_code['Date'][:10], d_page_code['Valute'][valute]['Value']))
            break


if __name__ == "__main__":
    required_valute = 'USD'

    parse_value(required_valute)
