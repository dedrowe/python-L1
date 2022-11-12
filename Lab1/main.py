import csv
import requests
import json
import logging

logger = logging.getLogger()
logger.setLevel('INFO')


def write_value_to_file(value: list, source="dataset.csv") -> None:
    """
    Функция записывает данные в таблицу

    source: название файла, в который будут записаны данные
    value: строка которая будет записана в таблицу
    """
    try:
        with open(source, 'a') as dataset:
            writer = csv.writer(dataset, dialect='unix')
            writer.writerow(value)
    except OSError as er:
        logging.warning(f'Ошибка открытия файла: {er}')


def parse_value(currency: str, min_date: str = '1992-07-01', source: str = 'https://www.cbr-xml-daily.ru/daily_json.js'
                ) -> None:
    """
    Функция получает данные с сайта до последней записи
    Сделать отслеживание прогресса через tqdm не получится, т.к. не известно конечное количество дней, которые
    потребуется считать

    currency: валюта, значение которой программа будет извлекать
    min_date: дата последней записи
    source: ссылка на запись
    """
    page_code = requests.get(source)
    d_page_code = json.loads(page_code.text)

    while d_page_code['Date'][:10] != min_date:
        page_code = requests.get("https:" + d_page_code['PreviousURL'])
        write_value_to_file([d_page_code['Date'][:10], d_page_code['Valute'][currency]['Value']])
        d_page_code = json.loads(page_code.text)
        logging.info(f'Программа сейчас на дате {d_page_code["Date"][:10]}, последняя дата: {min_date}')
    write_value_to_file([d_page_code['Date'][:10], d_page_code['Valute'][currency]['Value']])


if __name__ == "__main__":
    required_valute = 'USD'
    parse_value(required_valute)
