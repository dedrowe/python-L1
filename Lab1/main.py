import csv
import requests
import json


def file_input(value, data):
    """
    Функция записывает данные в таблицу
    """
    writer = csv.writer(data, dialect='unix')
    writer.writerow(value)


def take_value(source, temp_dataset):
    """
    Функция получает данные с сайта до даты 2020-02-08(это самая последняя запись)
    """
    page_code = requests.get(source)
    d_page_code = json.loads(page_code.text)

    while True:
        page_code = requests.get("https:" + d_page_code['PreviousURL'])
        file_input((d_page_code['Date'][:10], d_page_code["Valute"]['USD']['Value']), temp_dataset)
        d_page_code = json.loads(page_code.text)
        if d_page_code['Date'][:10] == "2020-02-08":
            file_input((d_page_code['Date'][:10], d_page_code['Valute']['USD']['Value']), temp_dataset)
            break


if __name__ == "__main__":
    dataset = open("dataset.csv", 'a')
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    take_value(url, dataset)
    dataset.close()
